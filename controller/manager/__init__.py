import logging
import zmq
import time
import json
import model
import plugin
import ap_manager_client
import updater
from api.errors import *


UPDATE_ACTIONS = ["post", "put", "delete", "periodic_update"]


class ResourceManager(object):

    def __init__(self, params):
        self.params = params
        # load configuration
        model.load_config(params.config, basepath=params.path)
        # connect to database
        model.connect_db()
        # clear db
        model.ue.UE.drop_collection()
        model.location.Location.drop_collection()
        model.accesspoint.AccessPoint.drop_collection()
        # setup zero mq receiver
        self.setup_zmq()
        # load access point definitions from configuration file
        # and from remote AP manager component.
        # Deletes all current AP definitions at first.
        # If connection to remote AP manage API is not possible,
        # the system will run without any AP object and thus
        # no APs are assigned to UEs.
        model.accesspoint.AccessPoint.refresh(
            model.CONFIG["accesspoints"], ap_manager_client.get_accesspoints())
        # load management algorithm
        plugin.load_algorithms(
            model.CONFIG["algorithm"]["available"],
            model.CONFIG["algorithm"]["default"])
        # kick of AP state fetcher thread
        self.apFetcherThread = updater.AccessPointStateFetcher()
        self.apFetcherThread.start()

    def setup_zmq(self):
        context = zmq.Context()
        self.zmqreceiver = context.socket(zmq.PULL)
        constr = "tcp://*:%d" % (model.CONFIG["zmq"]["port"])
        self.zmqreceiver.bind(constr)
        logging.info("Create ZMQ receiver: %s" % constr)

    def run(self):
        """
        run endless ZMQ receiver loop and react on incoming update messages
        """
        logging.info("Running ResourceManager instance...")
        last_message = None
        while True:
            # try to receive ALL pending ZMQ messages
            try:
                last_message = self.zmqreceiver.recv(flags=zmq.NOBLOCK)
                # do not miss special messages
                if json.loads(last_message).get("action") == "delete":
                    raise Exception
                continue
            except:
                if last_message is None:
                    time.sleep(0.1)
            # there was at least one ZMQ message, process it
            if last_message is not None:
                data = json.loads(last_message)
                last_message = None
                logging.info("Received: %s" % str(data))
                if "action" in data:
                    # process UE related update
                    if data["action"] in UPDATE_ACTIONS:
                        self.dispatch_update_notification(data)
                    # process algorithm switch
                    if data["action"] == "switch_algorithm":
                        if "algorithm" in data:
                            plugin.switch_algorithm(data["algorithm"])

    def dispatch_update_notification(self, data):
        """
        This is executed if an update message was received by ZMQ.
        (e.g. new UE in system, or location changed, ...)

        Runs the optimization plugin to compute:
            a) Power management: Which APs are on or off?
            b) Assignment: Which UE connects to which AP?
        """
        # fetch data from request
        req_ue = None
        if "ue" in data:
            req_ue = data["ue"]

        # fetch data from DB
        ue_list = [ue.marshal().copy() for ue in model.ue.UE.objects]
        ap_list = [ap.marshal().copy()
                   for ap in model.accesspoint.AccessPoint.objects]

        # special case, remove mac address from network manager if
        # the request is a delete request and the UE is not present anymore
        if data["action"] == "delete":
            remove_mac = data.get("mac")
            if remove_mac is not None:
                # trigger AP manager component
                ap_manager_client.set_mac_list(
                    remove_mac,
                    [],
                    [ap.get("uuid") for ap in ap_list])
                logging.info("UE deleted. Removing MAC: %s from APs: %s"
                             % (remove_mac,
                                [ap.get("uuid") for ap in ap_list]))

        #######################################################################
        # run algorithms
        if len(plugin.algorithm_list) < 1:
            raise Exception("No resource management algorithm loaded.")
        # always run all available algorithms and only use the result of the selected afterwards
        results = {}
        for algorithm in plugin.algorithm_list:
            logging.info("=" * 15 + " START " + "=" * 15)
            if algorithm is None:
                raise Exception("Executed algorithm is None")
            results[algorithm.name] = algorithm.compute(ue_list, ap_list, req_ue)
            assert(len(results[algorithm.name]) > 1)
            logging.info("=" * 15 + " END " + "=" * 15)

        if plugin.selected_algorithm is None:
            raise Exception("No algorithm selected")
        if plugin.selected_algorithm not in results:
            raise Exception("Result of selected algorithm is not available")
        # use result of currently selected algorithm
        result = results[plugin.selected_algorithm]
        logging.info("=" * 15 + " RESULT " + "=" * 15)
        logging.info("Using result from: %s" % str(plugin.selected_algorithm))
        logging.info("Result: power control: %s" % str(result[0]))
        logging.info("Result: Assignment: %s" % str(result[1]))
        #######################################################################
        # trigger ap manager and update model with results and store them
        self.apply_power_control_result(result[0])
        self.apply_assignment_result(result[1])

    def apply_power_control_result(self, result):
        """
        Apply power control result:
            1. Trigger the AP manager in order to change the power state
               of the corresponding access point.
               (Only done if a power_state has changed)
            2. Apply changes to model and store it in the DB.
        """
        for uuid, state in result.items():  # iterate all power states
            try:
                power_state = 1 if state else 0

                # if we have a changed power_state, we trigger the AP manger
                if model.accesspoint.AccessPoint.objects.get(
                        uuid=uuid).power_state != power_state:
                    # trigger AP manager component
                    ap_manager_client.set_power_state(uuid, state)

                # update model (should be atomic update!)
                model.accesspoint.AccessPoint.objects(uuid=uuid).update_one(
                    set__power_state=power_state)
            except:
                # can fail if access point was deleted
                logging.warning("Power state update failed.")

    def apply_assignment_result(self, result):
        """
        Apply assignment result:
            1. Trigger MAC address black and white listing at the AP manager
               component to ensure that UEs can only connect to assigned APs.
               (Only done if assignment has changed)
            2. Apply changes to model and store it in the DB.
            3. TODO: Trigger notification of UE, so that it can pull the
               assignment result in order to (re)connect to the right AP.
        """
        # fill up the assignment result with UEs not assigned to APs
        # (we need a complete UE to update our model)
        for ue_uuid in [ue.uuid for ue in model.ue.UE.objects]:
            if ue_uuid not in result:
                result[ue_uuid] = None  # add 'not assigned' entries

        for ue_uuid, ap_uuid in result.items():  # iterate all assignments
            try:
                ue = model.ue.UE.objects.get(uuid=ue_uuid)
                assigned_ap_uuid = ue.assigned_accesspoint.uuid if (
                    ue.assigned_accesspoint is not None) else None
                # if the assignment has changed, trigger MAC list update at AP
                if assigned_ap_uuid != ap_uuid:
                    # list of assigned AP UUIDs
                    enable_on = [ap.uuid for ap
                                 in model.accesspoint.AccessPoint.objects
                                 if ap.uuid == ap_uuid]
                    # list of not assigned AP UUIDs
                    disable_on = [ap.uuid for ap
                                  in model.accesspoint.AccessPoint.objects
                                  if ap.uuid != ap_uuid]
                    # trigger AP manager component
                    ap_manager_client.set_mac_list(
                        ue.wifi_mac,
                        enable_on,
                        disable_on)

                # update model
                if ap_uuid is None:
                    ue.remove_accesspoint()
                else:
                    try:
                        ap = model.accesspoint.AccessPoint.objects.get(
                            uuid=ap_uuid)
                        ue.assign_accesspoint(ap)
                    except:
                        # can fail if ue was deleted
                        logging.exception("Assignment model update failed.")
            except:
                # can fail if ue was deleted
                logging.exception("Assignment update failed.")

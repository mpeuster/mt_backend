import logging
import zmq
import time
import json
import model
import plugin
import ap_manager_client
from api.errors import *


UPDATE_ACTIONS = ["post", "put", "delete"]


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
        plugin.load_algorithm(model.CONFIG["algorithm"]["name"])

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
        while True:
            r = self.zmqreceiver.recv()
            data = json.loads(r)
            logging.debug("Received: %s" % str(data))
            if "action" in data:
                if data["action"] in UPDATE_ACTIONS:
                    self.dispatch_update_notification(data)

    def dispatch_update_notification(self, data):
        """
        This is executed if an update message was received by ZMQ.
        (e.g. new UE in system, or location changed, ...)

        Runs the optimization plugin to compute:
            a) Power management: Which APs are on or off?
            b) Assignment: Which UE connects to which AP?
        """
        # fetch data from DB
        ue_list = [ue.marshal().copy() for ue in model.ue.UE.objects]
        ap_list = [ap.marshal().copy()
                   for ap in model.accesspoint.AccessPoint.objects]

        #######################################################################
        # run algorithm
        if plugin.algorithm is None:
            raise Exception("No resource management algorithm loaded.")
        result = plugin.algorithm.compute(ue_list, ap_list, data["ue"])
        assert(len(result) > 1)
        logging.info("=" * 40)
        logging.info("Result: power control: %s" % str(result[0]))
        logging.info("Result: Assignment: %s" % str(result[1]))
        logging.info("=" * 40)
        #######################################################################
        # trigger ap manager and update model with results and store them
        self.apply_power_control_result(result[0])
        self.apply_assignment_result(result[1])

    def apply_power_control_result(self, result):
        """
        Apply power control result:
            1. Trigger the AP manager in order to change the power state
               of the corresponding access point.
               (Only done if a pwoer_state has changed)
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

                # if the assignment has changed, trigger MAC list update at AP
                if ((ue.assigned_accesspoint is None and ap_uuid is not None)
                        or ue.assigned_accesspoint.uuid != ap_uuid):
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

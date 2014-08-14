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
        logging.info("Running ResourceManager instance...")
        # run endless ZMQ receiver loop and react on incoming update messages
        while True:
            r = self.zmqreceiver.recv()
            data = json.loads(r)
            logging.debug("Received: %s" % str(data))
            if "action" in data:
                if data["action"] in UPDATE_ACTIONS:
                    self.dispatch_update_notification(data)

    def dispatch_update_notification(self, data):
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
        for uuid, state in result[0].items():  # iterate all power states
            try:
                power_state = 1 if state else 0

                # if we have a changed power_state, we trigger the AP manger
                if not model.accesspoint.AccessPoint.objects.get(
                        uuid=uuid).power_state == power_state:
                    # trigger AP manager component
                    ap_manager_client.set_power_state(uuid, state)

                # update model (should be atomic update!)
                model.accesspoint.AccessPoint.objects(uuid=uuid).update_one(
                    set__power_state=power_state)
            except:
                # can fail if access point was deleted
                logging.warning("Power state update failed.")

        for ue_uuid, ap_uuid in result[1].items():  # iterate all assignments
            try:
                ue = model.ue.UE.objects.get(uuid=ue_uuid)
                if ap_uuid is None:
                    ue.remove_accesspoint()
                else:
                    try:
                        ap = model.accesspoint.AccessPoint.objects.get(
                            uuid=ap_uuid)
                        ue.assign_accesspoint(ap)
                    except:
                        # can fail if ue was deleted
                        logging.warning("Assignment update failed.")
            except:
                # can fail if ue was deleted
                logging.warning("Assignment update failed.")

        # TODO: trigger AP power control
        # TODO: trigger UE update notification

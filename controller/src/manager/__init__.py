import logging
import zmq
import time
import json
import model
import plugin
from api.errors import *


UPDATE_ACTIONS = ["post", "put", "delete"]


class NetworkManager(object):

    def __init__(self, params):
        self.params = params
        # load configuration
        model.load_config(params.config, basepath=params.path)
        # connect to database
        model.connect_db()
        # setup zero mq receiver
        self.setup_zmq()
        # load management algorithm
        plugin.load_algorithm(model.CONFIG["algorithm"]["name"])

    def setup_zmq(self):
        context = zmq.Context()
        self.zmqreceiver = context.socket(zmq.PULL)
        constr = "tcp://*:%d" % (model.CONFIG["zmq"]["port"])
        self.zmqreceiver.bind(constr)
        logging.info("Create ZMQ receiver: %s" % constr)

    def run(self):
        logging.info("Running NetworkManager instance...")

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

        # update model with results and store them into DB
        for uuid, state in result[0].items():  # iterate all power states
            try:
                power_state = 1 if state else 0
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

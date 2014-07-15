import logging
import zmq
import time
import json
import model
import plugin


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
                pass
                if data["action"] in UPDATE_ACTIONS:
                    self.dispatch_update_notification(data)

    def dispatch_update_notification(self, data):
        # fetch data from DB
        ue_list = [ue.marshal() for ue in model.ue.UE.objects]
        ap_list = [ap.marshal()
                   for ap in model.accesspoint.AccessPoint.objects]
        # run algorithm
        plugin.algorithm.compute(ue_list, ap_list, data["ue"])

        # store results
        # trigger AP power control
        # trigger UE update notification

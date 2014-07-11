import logging
import zmq
import time
import model


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
        self.zmqreceiver.bind("tcp://*:5557")

    def run(self):
        logging.info("Running NetworkManager instance...")

        while True:
            s = self.zmqreceiver.recv()
            logging.info("Received: %s" % str(s))
            logging.info("Starting work ... ")
            time.sleep(0.01)
            logging.info("... finished!")

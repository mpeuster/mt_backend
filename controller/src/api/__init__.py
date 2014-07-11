import logging
import zmq
from api.errors import *
import api


def check_required_fields(data, required_keys):
    for k in required_keys:
        if k not in data:
            raise RequestDataError("Key missing: %s" % k)


ZMQ_SENDER = None


def setup_zmq():
    context = zmq.Context()
    api.ZMQ_SENDER = context.socket(zmq.PUSH)
    api.ZMQ_SENDER.connect("tcp://localhost:5557")
    logging.info("Create ZMQ sender: %s" % "tcp://localhost:5557")


def zmq_send(data):
    if ZMQ_SENDER is not None:
        logging.debug("Sending to ZMQ: %s" % str(data))
        api.ZMQ_SENDER.send(data)

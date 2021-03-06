import api
import logging
import threading
import time
import json
import zmq
from flask import Flask
from flask.ext import restful
import resources.ue
import resources.location
import resources.accesspoint
import resources.algorithm
import model
import api
import errors


def check_required_fields(data, required_keys):
    for k in required_keys:
        if k not in data:
            raise errors.RequestDataError("Key missing: %s" % k)


ZMQ_SENDER = None


CORS_HEADER = {'Access-Control-Allow-Origin': '*'}


def setup_zmq():
    context = zmq.Context()
    api.ZMQ_SENDER = context.socket(zmq.PUSH)
    constr = "tcp://%s:%d" % (model.CONFIG["zmq"]["host"],
                              model.CONFIG["zmq"]["port"])
    api.ZMQ_SENDER.connect(constr)
    logging.info("Create ZMQ sender: %s" % constr)


def zmq_send(data):
    if ZMQ_SENDER is not None:
        logging.debug("Sending to ZMQ: %s" % str(data))
        api.ZMQ_SENDER.send(data)


class PeriodicUpdater(threading.Thread):
    """
    Thread that sends periodic update signal to controller.
    Used to ensure that the controller runs from time to time
    and checks the testbed's system state.
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.INTERVAL = 8

    def run(self):
        while True:
            # send update notification over ZMQ
            api.zmq_send(json.dumps({"action": "periodic_update"}))
            # wait for next periodic update
            time.sleep(self.INTERVAL)


class APIServer(object):

    def __init__(self, params):
        self.params = params
        # load configuration
        model.load_config(params.config, basepath=params.path)
        # connect to database
        model.connect_db()
        # setup zero mq sender
        api.setup_zmq()

    def run(self):
        # setups
        self.setup_application()
        self.setup_api()
        # start periodic update thread
        pa = api.PeriodicUpdater()
        pa.start()
        # start API server
        if False:
            # default server:
            logging.info("API Server: Pure Flask")
            self.app.run(debug=False, use_reloader=False,
                         port=model.CONFIG["api"]["port"])
        elif False:
            logging.info("API Server: Gevent")
            from gevent.wsgi import WSGIServer
            http_server = WSGIServer(('',
                                     model.CONFIG["api"]["port"]),
                                     self.app)
            http_server.serve_forever()
        else:
            logging.info("API Server: Tornado")
            from tornado.wsgi import WSGIContainer
            from tornado.httpserver import HTTPServer
            from tornado.ioloop import IOLoop
            http_server = HTTPServer(WSGIContainer(self.app))
            http_server.listen(model.CONFIG["api"]["port"])
            IOLoop.instance().start()

    def setup_application(self):
        self.app = Flask(__name__)
        self.api = restful.Api(self.app, errors=errors.error_messages)

    def setup_api(self):
        # UE
        self.api.add_resource(resources.ue.UEList,
                              "/api/ue", endpoint="ue_list")
        self.api.add_resource(resources.ue.UE,
                              "/api/ue/<string:uuid>", endpoint="ue")
        # location
        self.api.add_resource(resources.location.Location,
                              "/api/location", endpoint="location")
        # access points
        self.api.add_resource(resources.accesspoint.APList,
                              "/api/accesspoint", endpoint="accesspoint_list")
        self.api.add_resource(resources.accesspoint.AP,
                              "/api/accesspoint/<string:uuid>",
                              endpoint="accesspoint")
        # algorithm
        self.api.add_resource(resources.algorithm.AlgorithmList,
                              "/api/algorithm", endpoint="algorithm_list")
        self.api.add_resource(resources.algorithm.SelectedAlgorithm,
                              "/api/algorithm/selected", endpoint="algorithm_selected")

import api
import logging
import zmq
from flask import Flask
from flask.ext import restful
import resources.ue
import resources.location
import resources.accesspoint
import model
import api
import errors


def check_required_fields(data, required_keys):
    for k in required_keys:
        if k not in data:
            raise RequestDataError("Key missing: %s" % k)


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
        self.setup_application()
        self.setup_api()

        if False:
            # default server:
            self.app.run(debug=True, use_reloader=False,
                         port=model.CONFIG["api"]["port"])
        else:
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
        # UE contexts
        self.api.add_resource(resources.ue.ContextList,
                              "/api/ue/<string:uuid>/context",
                              endpoint="context_list")
        self.api.add_resource(resources.ue.Context,
                              "/api/ue/<string:uuid>/context/<int:cid>",
                              endpoint="context")
        # location
        self.api.add_resource(resources.location.Location,
                              "/api/location", endpoint="location")
        # access points
        self.api.add_resource(resources.accesspoint.APList,
                              "/api/accesspoint", endpoint="accesspoint_list")
        self.api.add_resource(resources.accesspoint.AP,
                              "/api/accesspoint/<string:uuid>",
                              endpoint="accesspoint")

import logging
from flask import Flask
from flask.ext import restful
import resources.ue
import resources.location
import resources.accesspoint
import model
import api
import errors


class APIServer(object):

    def __init__(self, params):
        self.params = params
        # load configuration
        model.load_config(params.config, basepath=params.path)
        # connect to database
        model.connect_db()
        # setup zero mq sender
        api.setup_zmq()
        # load access point definitions from configuration file
        model.accesspoint.AccessPoint.load_from_config(
            model.CONFIG["accesspoints"])

    def run(self):
        self.setup_application()
        self.setup_api()

        if False:
            # default server:
            self.app.run(debug=True, use_reloader=False)
        else:
            # gevent:
            # from gevent.wsgi import WSGIServer
            # http_server = WSGIServer(('', 5000), self.app)
            # http_server.serve_forever()
            # tornado:
            from tornado.wsgi import WSGIContainer
            from tornado.httpserver import HTTPServer
            from tornado.ioloop import IOLoop
            http_server = HTTPServer(WSGIContainer(self.app))
            http_server.listen(5000)
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

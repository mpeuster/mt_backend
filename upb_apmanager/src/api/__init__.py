import api
import logging
from flask import Flask
from flask.ext import restful
import resources.accesspoint
import model
import api
import errors


def check_required_fields(data, required_keys):
    for k in required_keys:
        if k not in data:
            raise RequestDataError("Key missing: %s" % k)


class APIServer(object):

    def __init__(self, params):
        self.params = params
        # load configuration
        model.load_config(params.config, basepath=params.path)
        # load access point definitions from configuration file
        model.load_aps_from_config(
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
            http_server.listen(5001)  # TODO add port to config
            IOLoop.instance().start()

    def setup_application(self):
        self.app = Flask(__name__)
        self.api = restful.Api(self.app, errors=errors.error_messages)

    def setup_api(self):
        # access points
        self.api.add_resource(resources.accesspoint.APList,
                              "/api/network/accesspoint",
                              endpoint="accesspoint_list")
        self.api.add_resource(resources.accesspoint.AP,
                              "/api/network/accesspoint/<string:uuid>",
                              endpoint="accesspoint")
        self.api.add_resource(resources.accesspoint.PowerState,
                              "/api/network/accesspoint/<string:uuid>/power_state",
                              endpoint="accesspoint_power_state")

import api
import logging
from flask import Flask
from flask.ext import restful
import resources
import model
import api
import errors
import driver


def check_required_fields(data, required_keys):
    for k in required_keys:
        if k not in data:
            raise RequestDataError("Key missing: %s" % k)


class APIServer(object):

    def __init__(self, params):
        self.params = params
        # load configuration
        model.load_config(params.config, basepath=params.path)
        # load AP driver
        driver.load(model.CONFIG["driver"])
        # load access point definitions from configuration file
        model.load_aps_from_config(
            model.CONFIG["accesspoints"])

    def run(self):
        self.setup_application()
        self.setup_api()

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
        # access points
        self.api.add_resource(
            resources.APList,
            "/api/network/accesspoint",
            endpoint="accesspoint_list")
        self.api.add_resource(
            resources.AP,
            "/api/network/accesspoint/<string:uuid>",
            endpoint="accesspoint")
        self.api.add_resource(
            resources.PowerState,
            "/api/network/accesspoint/<string:uuid>/power_state",
            endpoint="accesspoint_power_state")
        self.api.add_resource(
            resources.Info,
            "/api/network/accesspoint/<string:uuid>/info",
            endpoint="accesspoint_info")
        self.api.add_resource(
            resources.Stats,
            "/api/network/accesspoint/<string:uuid>/stats",
            endpoint="accesspoint_stats")
        self.api.add_resource(
            resources.Client,
            "/api/network/client/<string:mac>",
            endpoint="client_mac")

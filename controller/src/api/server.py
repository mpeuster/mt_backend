import logging
from flask import Flask
from flask.ext import restful
import resources.ue
import model
import errors



class APIServer(object):

    def __init__(self, params):
        self.params = params
        self.model = model.SystemModel.get_instance()

    def run(self):
        self.setup_application()
        self.setup_api()   

        if False:
            # default server:
            self.app.run(debug=True, use_reloader=False)
        else:  
        # gevent:
        #from gevent.wsgi import WSGIServer
        #http_server = WSGIServer(('', 5000), self.app)
        #http_server.serve_forever()
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
        resources.ue.UEList.ENDPOINT_URL = "/api/ue"
        self.api.add_resource(resources.ue.UEList, "/api/ue", endpoint="ue_list")
        resources.ue.UE.ENDPOINT_URL = "/api/ue/"
        self.api.add_resource(resources.ue.UE, "/api/ue/<string:ue_id>", endpoint="ue")
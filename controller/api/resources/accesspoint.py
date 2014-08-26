import json
import logging
from flask import request
from flask.ext import restful
import model


class APList(restful.Resource):

    def get(self):
        l = ["%s" % ap.uri
             for ap in model.accesspoint.AccessPoint.objects]
        return l


class AP(restful.Resource):

    def get(self, uuid):
        ap = model.accesspoint.AccessPoint.get(uuid)
        json_data = ap.marshal()
        logging.debug("GET AP response body: %s", str(json_data))
        return json_data

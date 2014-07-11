import json
import logging
from flask import request
from flask.ext import restful
import model


class APList(restful.Resource):

    def get(self):
        l = ["%s" % ap.uri
             for ap in model.accesspoint.AccessPoint.objects]
        return json.dumps(l)


class AP(restful.Resource):

    def get(self, uuid):
        ap = model.accesspoint.AccessPoint.get(uuid)
        json_string = json.dumps(ap.marshal())
        logging.debug("GET AP response body: %s", json_string)
        return json_string

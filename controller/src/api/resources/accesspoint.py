import json
import logging
from flask import request
from flask.ext import restful
import model


class APList(restful.Resource):

    ENDPOINT_URL = ""

    def get(self):
        l = ["%s/%s" % (APList.ENDPOINT_URL, ap.uuid)
             for ap in model.AccessPoint.objects]
        return json.dumps(l)


class AP(restful.Resource):

    ENDPOINT_URL = ""

    def get(self, uuid):
        ap = model.AccessPoint.get(uuid)
        json_string = json.dumps(ap.marshal())
        logging.debug("GET AP response body: %s", json_string)
        return json_string

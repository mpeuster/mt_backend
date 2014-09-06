import json
import logging
from flask import request
from flask.ext import restful
import model
import api


class APList(restful.Resource):

    def get(self):
        l = ["%s" % ap.uri
             for ap in model.accesspoint.AccessPoint.objects]
        return l, 200, api.api.CORS_HEADER

    def options(self):
        return ({'Allow': 'GET'}, 200,
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'GET'})


class AP(restful.Resource):

    def get(self, uuid):
        ap = model.accesspoint.AccessPoint.get(uuid)
        json_data = ap.marshal()
        logging.debug("GET AP response body: %s", str(json_data))
        return json_data, 200, api.api.CORS_HEADER

    def options(self):
        return ({'Allow': 'GET'}, 200,
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'GET'})

import json
import logging
import time
import threading
from flask import request
from flask.ext import restful
from flask.ext.restful import fields, marshal
import model
from api.errors import JsonRequestParsingError


UE_RESOURCE_FIELDS = {
    'uuid': fields.String,
    'device_id': fields.String,
    'location_service_id': fields.String,
    'position_x': fields.Integer,
    'position_y': fields.Integer,
    'display_state': fields.Integer,
    'active_application': fields.String,
}


class UEList(restful.Resource):

    ENDPOINT_URL = ""

    def __init__(self):
        self.model = model.get_instance()

    def get(self):
        l = ["%s/%s" % (UEList.ENDPOINT_URL, k)
             for k in self.model.get_ue_dict().iterkeys()]
        return json.dumps(l)

    def post(self):
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("POST request body: %s" % str(json_data))
        # create UE in model
        new_ue = self.model.create_ue(json_data)
        # return URL of new UE with HTTP code 201: Created
        return json.dumps(["%s/%s" % (UEList.ENDPOINT_URL, new_ue.uuid)]), 201


class UE(restful.Resource):

    ENDPOINT_URL = ""

    def __init__(self):
        self.model = model.get_instance()

    def get(self, uuid):
        ue = self.model.get_ue(uuid)
        json_string = json.dumps(marshal(ue, UE_RESOURCE_FIELDS))
        logging.debug("GET response body: %s", json_string)
        return json_string

    def put(self, uuid):
        ue = self.model.get_ue(uuid)
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("PUT request body: %s" % str(json_data))
        ue.update(json_data)
        return None, 204

    def delete(self, uuid):
        if self.model.get_ue(uuid):
            del self.model.get_ue_dict()[uuid]
        return None, 204

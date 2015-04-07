import json
import logging
from flask import request, jsonify
from flask.ext import restful
import api
import model
from api.errors import JsonRequestParsingError


REQUIRED_FIELDS = [
    "device_id",
    "location_service_id",
    "display_state",
    "wifi_mac"
]


class UEList(restful.Resource):

    def get(self):
        l = ["%s" % ue.uri
             for ue in model.ue.UE.objects]
        return l, 200, api.CORS_HEADER

    def post(self):
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("POST UE request body: %s" % str(json_data))
        # validate data
        api.check_required_fields(json_data, REQUIRED_FIELDS)
        # create UE in model
        new_ue = model.ue.UE.create(json_data)
        # send update signal
        api.zmq_send(json.dumps({"action": "post", "ue": new_ue.uuid}))
        # return URL of new UE with HTTP code 201: Created
        return ["%s" % new_ue.uri], 201, api.CORS_HEADER

    def options(self):
        return ({'Allow': 'POST,GET'}, 200,
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'POST,GET'})


class UE(restful.Resource):

    def get(self, uuid):
        ue = model.ue.UE.get(uuid)
        json_data = ue.marshal()
        logging.debug("GET UE response body: %s", str(json_data))
        return json_data, 200, api.CORS_HEADER

    def put(self, uuid):
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("PUT UE request body: %s" % str(json_data))
        # validate data
        api.check_required_fields(json_data, REQUIRED_FIELDS)
        # update model
        model.ue.UE.update(uuid, json_data)
        # send update signal
        # api.zmq_send(json.dumps({"action": "put", "ue": uuid}))
        return None, 204, api.CORS_HEADER

    def delete(self, uuid):
        ue = model.ue.UE.get(uuid)
        model.ue.UE.get(uuid).delete()
        # send update signal
        api.zmq_send(json.dumps({"action": "delete",
                                "ue": uuid, "mac": ue.wifi_mac}))
        return None, 204, api.CORS_HEADER

    def options(self, uuid):
        return ({'Allow': 'PUT,GET,DELETE'}, 200,
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'PUT,GET,DELETE'})

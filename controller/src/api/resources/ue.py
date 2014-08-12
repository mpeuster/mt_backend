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
    "position_x",
    "position_y",
    "display_state",
    "wifi_mac"
]


class UEList(restful.Resource):

    def get(self):
        l = ["%s" % ue.uri
             for ue in model.ue.UE.objects]
        return l

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
        return ["%s" % new_ue.uri], 201


class UE(restful.Resource):

    def get(self, uuid):
        ue = model.ue.UE.get(uuid)
        json_data = ue.marshal()
        logging.debug("GET UE response body: %s", str(json_data))
        return json_data

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
        model.ue.UE.add_context(uuid, json_data)
        # send update signal
        api.zmq_send(json.dumps({"action": "put", "ue": uuid}))
        return None, 204

    def delete(self, uuid):
        model.ue.UE.get(uuid).delete()
        # send update signal
        api.zmq_send(json.dumps({"action": "delete", "ue": uuid}))
        return None, 204


class ContextList(restful.Resource):

    def get(self, uuid):
        ue = model.ue.UE.get(uuid)
        l = ["%s" % context.uri
             for context in ue.context_list]
        return l


class Context(restful.Resource):

    def get(self, uuid, cid):
        ue = model.ue.UE.get(uuid)
        json_data = ue.marshal(cid)
        logging.debug("GET UE/context response body: %s", str(json_data))
        return json_data

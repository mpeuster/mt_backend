import json
import logging
from flask import request
from flask.ext import restful
import model
from api.errors import JsonRequestParsingError


class UEList(restful.Resource):

    def get(self):
        l = ["%s" % ue.uri
             for ue in model.ue.UE.objects]
        return json.dumps(l)

    def post(self):
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("POST UE request body: %s" % str(json_data))
        # create UE in model
        new_ue = model.ue.UE.create(json_data)
        # return URL of new UE with HTTP code 201: Created
        return json.dumps(["%s" % new_ue.uri]), 201


class UE(restful.Resource):

    def get(self, uuid):
        ue = model.ue.UE.get(uuid)
        json_string = json.dumps(ue.marshal())
        logging.debug("GET UE response body: %s", json_string)
        return json_string

    def put(self, uuid):
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("PUT UE request body: %s" % str(json_data))
        ue = model.ue.UE.get(uuid)
        ue.update(json_data)
        ue.add_context(json_data)
        ue.save()
        return None, 204

    def delete(self, uuid):
        model.ue.UE.get(uuid).delete()
        return None, 204


class ContextList(restful.Resource):

    def get(self, uuid):
        ue = model.ue.UE.get(uuid)
        l = ["%s" % context.uri
             for context in ue.context_list]
        return json.dumps(l)


class Context(restful.Resource):

    def get(self, uuid, cid):
        ue = model.ue.UE.get(uuid)
        json_string = json.dumps(ue.marshal(cid))
        logging.debug("GET UE/context response body: %s", json_string)
        return json_string

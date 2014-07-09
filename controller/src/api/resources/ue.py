import json
import logging
from flask import request
from flask.ext import restful
import model
from api.errors import JsonRequestParsingError


class UEList(restful.Resource):

    ENDPOINT_URL = ""

    def get(self):
        l = ["%s/%s" % (UEList.ENDPOINT_URL, ue.uuid)
             for ue in model.UE.objects]
        return json.dumps(l)

    def post(self):
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("POST UE request body: %s" % str(json_data))
        # create UE in model
        new_ue = model.UE.create(json_data)
        # return URL of new UE with HTTP code 201: Created
        return json.dumps(["%s/%s" % (UEList.ENDPOINT_URL, new_ue.uuid)]), 201


class UE(restful.Resource):

    ENDPOINT_URL = ""

    def get(self, uuid):
        ue = model.UE.get(uuid)
        json_string = json.dumps(ue.marshal())
        logging.debug("GET UE response body: %s", json_string)
        return json_string

    def put(self, uuid):
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("PUT UE request body: %s" % str(json_data))
        ue = model.UE.get(uuid)
        ue.update(json_data)
        ue.add_context(json_data)
        ue.save()
        return None, 204

    def delete(self, uuid):
        model.UE.get(uuid).delete()
        return None, 204


class ContextList(restful.Resource):

    ENDPOINT_URL = ""

    def get(self, uuid):
        ue = model.UE.get(uuid)
        l = ["%s/%s/context/%s" %
             (ContextList.ENDPOINT_URL, uuid, ue.context_list.index(context))
             for context in ue.context_list]
        return json.dumps(l)


class Context(restful.Resource):

    ENDPOINT_URL = ""

    def get(self, uuid, cid):
        ue = model.UE.get(uuid)
        json_string = json.dumps(ue.marshal(cid))
        logging.debug("GET UE/context response body: %s", json_string)
        return json_string

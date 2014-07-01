import json
import logging
import time
import threading
from flask import request
from flask.ext import restful
from flask.ext.restful import fields, marshal
import model
from api.errors import *


class UEList(restful.Resource):

    ENDPOINT_URL = ""

    def __init__(self):
        self.model = model.get_instance()

    def get(self):
        l = ["%s/%s" % (UEList.ENDPOINT_URL, k) for k in self.model.get_ue_dict().iterkeys()]
        return json.dumps(l)

    def post(self):
        try:
            json_data = request.get_json(force=True)
        except:
           raise JsonRequestParsingError("Request parsing error")
        logging.debug("Request data: %s" % str(json_data))
        # create UE in model
        new_ue = self.model.create_ue(json_data)
        # return URL of new UE
        return json.dumps(["%s/%s" % (UEList.ENDPOINT_URL, new_ue.uuid)]), 201  # HTTP code 201: Created


class UE(restful.Resource):

    ENDPOINT_URL = ""

    def __init__(self):
        pass

    def get(self, ue_id):
        return json.dumps({})

    def put(self, ue_id):
        pass

    def delete(self, ue_id):
        pass



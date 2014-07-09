import json
import logging
from flask import request
from flask.ext import restful
import model
from api.errors import *


class Location(restful.Resource):

    ENDPOINT_URL = ""

    def __init__(self):
        pass

    def post(self):
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("POST location request body: %s" % str(json_data))
        # validate data
        # #TODO: create validation function (arg: List of required fields)
        if "location_service_id" not in json_data:
            raise RequestDataError("Missing: location_service_id")
        if "position_x" not in json_data:
            raise RequestDataError("Missing: position_x")
        if "position_y" not in json_data:
            raise RequestDataError("Missing: position_y")
        # update location entry in db
        (loc, _) = model.Location.objects.get_or_create(
            location_service_id=json_data["location_service_id"])
        loc.position_x = json_data["position_x"]
        loc.position_y = json_data["position_y"]
        loc.save()
        # trigger location update in all matching UE model entries
        for ue in model.UE.objects(
                location_service_id=loc.location_service_id):
            ue.pull_external_location()
            ue.save()
        return None, 201

import json
import logging
import api
from flask import request
from flask.ext import restful
import model
from api.errors import *


REQUIRED_FIELDS = [
    "location_service_id",
    "position_x",
    "position_y"
]


class Location(restful.Resource):

    def post(self):
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("POST location request body: %s" % str(json_data))
        # validate data
        api.check_required_fields(json_data, REQUIRED_FIELDS)
        # update location entry in db
        (loc, _) = model.location.Location.objects.get_or_create(
            location_service_id=json_data["location_service_id"])
        loc.position_x = json_data["position_x"]
        loc.position_y = json_data["position_y"]
        loc.save()
        # trigger location update in all matching UE model entries
        for ue in model.ue.UE.objects(
                location_service_id=loc.location_service_id):
            ue.pull_external_location()
            ue.save()
            # send update signal
            api.zmq_send(json.dumps({"action": "put", "ue": ue.uuid}))
        # trigger location update in all matching AP model entries
        for ap in model.accesspoint.AccessPoint.objects(
                location_service_id=loc.location_service_id):
            ap.position_x = loc.position_x
            ap.position_y = loc.position_y
            ap.save()
            logging.debug("Updated location of AP: %s" % str(ap.device_id))
        return None, 201

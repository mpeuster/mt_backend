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
        # ATTENTION: Location is only updated in UE context,
        # if the UE performs an update action!
        # trigger location update in all matching AP model entries
        model.accesspoint.AccessPoint.objects(
            location_service_id=loc.location_service_id).update(
                set__position_x=loc.position_x,
                set__position_y=loc.position_y
                )
        return None, 201, api.CORS_HEADER

    def options(self):
        return ({'Allow': 'POST'}, 200,
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'POST'})

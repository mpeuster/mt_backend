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
        # update location entry in location db
        (loc, _) = model.location.Location.objects.get_or_create(
            location_service_id=json_data["location_service_id"])
        loc.position_x = float(json_data["position_x"])
        loc.position_y = float(json_data["position_y"])
        loc.save(validate=False)
        # trigger location update on UE
        # (copy latest context and insert new one to use new location)
        for ue in model.ue.UE.objects(
                location_service_id=loc.location_service_id):
            model.ue.UE.update(ue.uuid, ue.marshal())
        # trigger location update in all matching AP model entries
        # (can be done directly for the APs)
        model.accesspoint.AccessPoint.objects(
            location_service_id=loc.location_service_id).update(
                set__position_x=loc.position_x,
                set__position_y=loc.position_y
                )
        # send update signal controller
        api.zmq_send(json.dumps({"action": "put", "ue": "location_service"}))
        return None, 201, api.CORS_HEADER

    def options(self):
        return ({'Allow': 'POST,PUT,GET,DELETE'}, 200,
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'POST,PUT,GET,DELETE',
                 'Access-Control-Allow-Headers': 'Content-Type'})

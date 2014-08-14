import json
import logging
from flask import request
from flask.ext import restful
import model
from api.errors import *


class APList(restful.Resource):

    def get(self):
        """
        Returns list of access points, grouped by usage availability.
        """
        result = {}
        result["online"] = [ap.uuid for ap in model.AccessPoints.itervalues()
                            if ap.state == "online"]
        result["offline"] = [ap.uuid for ap in model.AccessPoints.itervalues()
                             if ap.state == "offline"]
        return result


class AP(restful.Resource):

    def get(self, uuid):
        """
        Return details of access point taken from configuration file.
        """
        if uuid in model.AccessPoints:
            return model.AccessPoints[uuid].marshal()
        else:
            raise ResourceNotFoundError


class PowerState(restful.Resource):

    def get(self, uuid):
        """
        Returns power state of specific AP.
        """
        if uuid in model.AccessPoints:
            return {"power_state": model.AccessPoints[uuid].power_state}
        else:
            raise ResourceNotFoundError
        return "test"

    def put(self, uuid):
        """
        Sets the power state of a specific AP.
        """
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("PUT request body: %s" % str(json_data))
        if uuid not in model.AccessPoints:
            raise ResourceNotFoundError
        if "power_state" not in json_data:
            raise RequestDataError
        # request is valid change model
        model.AccessPoints[uuid].power_state = json_data["power_state"]
        return None, 204

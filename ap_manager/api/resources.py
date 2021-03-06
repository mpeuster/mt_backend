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
        if (json_data["power_state"] != "radio_on" and
                json_data["power_state"] != "radio_off"):
            raise RequestDataError
        # request is valid, change model
        model.AccessPoints[uuid].power_state = json_data["power_state"]
        return None, 204


class Info(restful.Resource):

    def get(self, uuid):
        """
        Return general info about access point. Serial, name, etc.
        """
        if uuid in model.AccessPoints:
            return model.AccessPoints[uuid].marshal()
        else:
            raise ResourceNotFoundError


class Stats(restful.Resource):

    def get(self, uuid):
        """
        Return network statistics of access point.
        May have some delay, since it first calls the AP and requests
        current data by using the driver layer.
        """
        if uuid in model.AccessPoints:
            return model.AccessPoints[uuid].get_network_stats()
        else:
            raise ResourceNotFoundError


class Client(restful.Resource):

    def put(self, mac):
        try:
            json_data = request.get_json(force=True)
        except:
            raise JsonRequestParsingError("Request parsing error")
        logging.debug("PUT request argument: %s", mac)
        logging.debug("PUT request body: %s" % str(json_data))

        # validate data
        if len(mac) < 12:
            raise RequestDataError
        for uuid in json_data["enable_on"]:
            if uuid not in model.AccessPoints:
                raise ResourceNotFoundError
        for uuid in json_data["disable_on"]:
            if uuid not in model.AccessPoints:
                raise ResourceNotFoundError

        # request is valid, change model
        for ap in model.AccessPoints.itervalues():
            if ap.uuid in json_data["enable_on"]:
                if mac not in ap.enabled_macs:
                    ap.enabled_macs.append(mac)
            else:
                if mac in ap.enabled_macs:
                    ap.enabled_macs.remove(mac)
            if ap.uuid in json_data["disable_on"]:
                if mac not in ap.disabled_macs:
                    ap.disabled_macs.append(mac)
            else:
                if mac in ap.disabled_macs:
                    ap.disabled_macs.remove(mac)
            # trigger mac black/white listing
            ap.trigger_mac_list_change()
        return None, 204

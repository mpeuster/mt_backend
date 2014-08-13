import json
import logging
from flask import request
from flask.ext import restful
import model


class APList(restful.Resource):

    def get(self):
        """
        Returns list of access points, grouped by usage availability.
        """
        pass
        return None


class AP(restful.Resource):

    def get(self, uuid):
        """
        Return details of access point taken from configuration file.
        """
        pass
        return None


class PowerState(restful.Resource):

    def get(self, uuid):
        """
        Returns power state of specific AP.
        """
        pass
        return None

    def put(self, uuid):
        """
        Sets the power state of a specific AP.
        """
        pass
        return None

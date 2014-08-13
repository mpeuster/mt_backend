import logging
import uuid
from flask.ext.restful import fields, marshal
import model

AP_RESOURCE_FIELDS = {
    'uuid': fields.String,
    'name': fields.String,
    'ssid': fields.String,
}


class AccessPoint():

    def __init__(
            self,
            name,
            ssid,
            state="offline"):
        # create uuid
        self.uuid = uuid.uuid1().hex
        # set parameter
        self.name = name
        self.ssid = ssid
        self.state = state
        self.power_state = "radio_off"
        self.enabled_macs = []
        self.disabled_macs = []

    def __repr__(self):
        return ("SSID=%s and UUID=%s") \
            % (self.ssid, self.uuid)

    def marshal(self):
        return marshal(self, AP_RESOURCE_FIELDS)

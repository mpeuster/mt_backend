import logging
import uuid
from flask.ext.restful import fields, marshal
import model
import driver

AP_RESOURCE_FIELDS = {
    'uuid': fields.String,
    'name': fields.String,
    'ssid': fields.String,
}


class AccessPoint(object):

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
        self._power_state = "radio_off"
        self.enabled_macs = []
        self.disabled_macs = []

    def __repr__(self):
        return ("SSID=%s and UUID=%s") \
            % (self.ssid, self.uuid)

    def marshal(self):
        return marshal(self, AP_RESOURCE_FIELDS)

    @property
    def power_state(self):
        return self._power_state

    @power_state.setter
    def power_state(self, value):
        if self._power_state != value:
            self._power_state = value
            # run the AP driver
            driver.AP_DRIVER.set_power_state(self)

    def trigger_mac_list_change(self):
        # run the AP driver
        driver.AP_DRIVER.set_mac_lists(self)

import logging
import uuid
from flask.ext.restful import fields, marshal
import model
import driver

AP_RESOURCE_FIELDS = {
    'uuid': fields.String,
    'state': fields.String
}


class AccessPoint(object):

    def __init__(
            self,
            uuid,
            state="offline",
            driver_info=None):
        # create uuid (use a fixed one, see mail with Alberto (MobiMash))
        self.uuid = uuid  # uuid.uuid1().hex
        # set parameter
        self.name = None  # not used
        self.ssid = None  # not used
        self.driver_info = driver_info  # dict, containing info. for driver
        self.state = state
        self._power_state = "radio_off"
        self.enabled_macs = []
        self.disabled_macs = []

        # clear mac lists on AP
        self.trigger_mac_list_change()

    def __repr__(self):
        return ("UUID=%s") \
            % self.uuid

    def marshal(self):
        return marshal(self, AP_RESOURCE_FIELDS)

    @property
    def power_state(self):
        return self._power_state

    @power_state.setter
    def power_state(self, value):
        if self._power_state != value and self.state == "online":
            self._power_state = value
            # run the AP driver
            driver.AP_DRIVER.set_power_state(self)

    def trigger_mac_list_change(self):
        # run the AP driver
        if self.state == "online":
            driver.AP_DRIVER.set_mac_lists(self)

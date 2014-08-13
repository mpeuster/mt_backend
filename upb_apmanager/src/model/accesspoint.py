import logging
import uuid
import model


class AccessPoint():

    def __init__(
            self,
            device_id,
            ssid,
            location_service_id=None,
            position_x=0,
            position_y=0,
            state="offline"):
        # create uuid
        self.uuid = uuid.uuid1().hex
        # set parameter
        self.device_id = device_id
        self.ssid = ssid
        self.location_service_id = location_service_id
        self.position_x = position_x
        self.position_y = position_y
        self.state = state
        self.power_state = "radio_off"
        self.enabled_macs = []
        self.disabled_macs = []

    def __repr__(self):
        return ("%s with SSID=%s and UUID=%s") \
            % (self.device_id, self.ssid, self.uuid)

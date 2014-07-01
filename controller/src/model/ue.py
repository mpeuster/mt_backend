import logging
import uuid

class UE(object):

    def __init__(self, json_data):
        self.uuid = uuid.uuid1().hex
        self.device_id = None
        self.location_service_id = None
        self.position_x = 0
        self.position_y = 0
        self.display_state = 0
        self.active_application = None

        if "device_id" in json_data:
            self.device_id = json_data["device_id"]


import logging
import uuid
from api.errors import RequestDataError


class UE(object):

    def __init__(self, json_data):
        self.uuid = uuid.uuid1().hex
        self.device_id = None
        self.location_service_id = None
        self.position_x = 0
        self.position_y = 0
        self.display_state = 0
        self.active_application = None

        self.update(json_data)

    def update(self, json_data):
        # TODO: can this be done automatically?
        try:
            self.device_id = json_data["device_id"]
            self.location_service_id = json_data["location_service_id"]
            self.position_x = json_data["position_x"]
            self.position_y = json_data["position_y"]
            self.display_state = json_data["display_state"]
            self.active_application = json_data["active_application"]
        except:
            raise RequestDataError("UE model data update error")

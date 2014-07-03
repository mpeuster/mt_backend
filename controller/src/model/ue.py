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
        try:
            for k, v in json_data.items():
                if k not in self.__dict__:
                    raise RequestDataError("Wrong request data key")
                self.__dict__[k] = v
        except:
            raise RequestDataError("UE model data update error")

import logging
import datetime
from mongoengine import *
from api.errors import RequestDataError


class Context(EmbeddedDocument):
    # system fields
    created = DateTimeField(default=datetime.datetime.now)
    # user fields
    position_x = IntField(default=0)
    position_y = IntField(default=0)
    display_state = IntField(default=0)
    active_application = StringField(default=None)


class UE(Document):
    # system fields
    uuid = StringField(required=True, unique=True, primary_key=True)
    # user fields
    device_id = StringField(required=True, unique=True)
    location_service_id = StringField(default=None)
    # references
    context_list = SortedListField(EmbeddedDocumentField(Context))

    def update_with_json(self, json_data):
        self.device_id = json_data["device_id"]
        self.location_service_id = json_data["location_service_id"]

    def add_context(self, json_data):
        new_c = Context()
        new_c.position_x = json_data["position_x"]
        new_c.position_y = json_data["position_y"]
        new_c.display_state = json_data["display_state"]
        new_c.active_application = json_data["active_application"]
        self.context_list.append(new_c)

    def get_response(self):
        res = {}
        logging.debug(str(self.__dict__))
        for k, v in self.__dict__["_data"].items():
            res[k] = v
        latest_context = self.context_list[-1]
        for k, v in latest_context.__dict__["_data"].items():
            res[k] = v
        return res

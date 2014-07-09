import logging
import datetime
import uuid
from mongoengine import *
from api.errors import *
from flask.ext.restful import fields, marshal
from location import Location

UE_RESOURCE_FIELDS = {
    'uuid': fields.String,
    'device_id': fields.String,
    'registered_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'location_service_id': fields.String,
    'position_x': fields.Float,
    'position_y': fields.Float,
    'display_state': fields.Integer,
    'active_application': fields.String,
    'assigned_accesspoint': fields.String
}


class Context(EmbeddedDocument):
    # system fields
    updated_at = DateTimeField(default=datetime.datetime.now)
    # user fields
    position_x = FloatField(default=0)
    position_y = FloatField(default=0)
    display_state = IntField(default=0)
    active_application = StringField(default=None)


class UE(Document):
    # system fields
    uuid = StringField(required=True, unique=True, primary_key=True)
    registered_at = DateTimeField(default=datetime.datetime.now)
    # user fields
    device_id = StringField(required=True, unique=True)
    location_service_id = StringField(default=None)
    # references
    context_list = SortedListField(EmbeddedDocumentField(Context))

    @staticmethod
    def create(json_data):
        try:
            ue = UE(uuid=uuid.uuid1().hex,
                    device_id=json_data['device_id'])
            ue.update(json_data)
            ue.add_context(json_data)
            ue.save()
        except NotUniqueError:
            raise ResourceAlreadyExistsError("UE with this device_id exists.")
        return ue

    @staticmethod
    def get(uuid):
        try:
            ue = UE.objects.get(uuid=uuid)
        except:
            ue = None
        if ue is None:
            raise ResourceNotFoundError("UE not found in model.")
        return ue

    def update(self, json_data):
        try:
            # TODO: Field key validation
            self.device_id = json_data["device_id"]
            self.location_service_id = json_data["location_service_id"]

        except KeyError:
            raise RequestDataError("Field not found")
        except:
            raise RequestError("Error during update.")

    def add_context(self, json_data):
        try:
            new_c = Context()
            new_c.position_x = json_data["position_x"]
            new_c.position_y = json_data["position_y"]
            new_c.display_state = json_data["display_state"]
            new_c.active_application = json_data["active_application"]
            self.context_list.append(new_c)
        except KeyError:
            raise RequestDataError("Field not found")
        except:
            raise RequestError("Error during update.")
        self.pull_external_location()

    def pull_external_location(self):
        """
        Pulls latest location data from the 3rd party location service,
        stored in the model, if a location_service_id and a context is present.
        The location is stored in the latest context object.
        """
        if self.location_service_id is not None and len(self.context_list) > 0:
            try:
                loc = Location.objects.get(
                    location_service_id=self.location_service_id)
            except:
                loc = None
            if loc:
                context = self.context_list[-1]
                context.position_x = loc.position_x
                context.position_y = loc.position_y
                logging.debug("External location inserted into UE: %s"
                              % str(self.device_id))

    def marshal(self, cid=-1):
        """
        Builds the json representation of a UE with the selected context.
        If cid = -1 the latest context is returned.
        """
        res = {}
        logging.debug(str(self.__dict__))
        for k, v in self.__dict__["_data"].items():
            res[k] = v
            context = self.context_list[cid]
        for k, v in context.__dict__["_data"].items():
            res[k] = v
        return marshal(res, UE_RESOURCE_FIELDS)

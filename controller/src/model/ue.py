import logging
import datetime
import uuid
import model
from mongoengine import *
from api.errors import *
from flask.ext.restful import fields, marshal

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
    'assigned_accesspoint': fields.String,
    'uri': fields.String,
    'wifi_mac': fields.String
}


class Context(EmbeddedDocument):
    # system fields
    updated_at = DateTimeField(default=datetime.datetime.now)
    # user fields
    position_x = FloatField(default=-1)
    position_y = FloatField(default=-1)
    display_state = IntField(default=0)
    active_application = StringField(default=None)

    def get_parent_ue(self):
        for ue in UE.objects:
            if self in ue.context_list:
                return ue

    @property
    def uri(self):
        ue = self.get_parent_ue()
        return "%s/%s/context/%s" % ("/api/ue",
                                     ue.uuid, ue.context_list.index(self))


class UE(Document):
    # system fields
    uuid = StringField(required=True, unique=True, primary_key=True)
    registered_at = DateTimeField(default=datetime.datetime.now)
    # user fields
    device_id = StringField(required=True, unique=True)
    location_service_id = StringField(default=None)
    wifi_mac = StringField(default=None)
    # references
    context_list = SortedListField(EmbeddedDocumentField(Context))
    assigned_accesspoint = ReferenceField(
        model.accesspoint.AccessPoint, default=None)

    @staticmethod
    def create(json_data):
        try:
            new_uuid = uuid.uuid1().hex
            ue = UE(uuid=new_uuid,
                    device_id=json_data['device_id'])
            ue.save()
            UE.update(new_uuid, json_data)
            UE.add_context(new_uuid, json_data)

        except NotUniqueError:
            logging.exception("Error:")
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

    @staticmethod
    def update(uuid, json_data):
        try:
            # atomic update of ue entry
            UE.objects(uuid=uuid).update_one(
                set__device_id=json_data["device_id"],
                set__location_service_id=json_data["location_service_id"],
                set__wifi_mac=json_data["wifi_mac"]
                )
        except:
            raise RequestError("Error during update.")

    @staticmethod
    def add_context(uuid, json_data):
        try:
            new_c = Context()
            new_c.position_x = json_data["position_x"]
            new_c.position_y = json_data["position_y"]
            new_c.display_state = json_data["display_state"]
            new_c.active_application = json_data["active_application"]
            # try to use third party location if available
            try:
                loc = model.location.Location.objects.get(
                    location_service_id=json_data["location_service_id"])
                new_c.position_x = loc.position_x
                new_c.position_y = loc.position_y
            except:
                logging.debug("Could not find location info for %s."
                              % json_data["location_service_id"])
            # atomic update of ue entry
            UE.objects(uuid=uuid).update_one(
                push__context_list=new_c)
        except:
            logging.exception("Error:")
            raise RequestError("Error during update.")

    @property
    def uri(self):
        return "%s/%s" % ("/api/ue", self.uuid)

    def marshal(self, cid=-1):
        """
        Builds the json representation of a UE with the selected context.
        If cid = -1 the latest context is returned.
        """
        res = {}
        for k, v in self.__dict__["_data"].items():
            res[k] = v
        if len(self.context_list) > 0:
            context = self.context_list[cid]
            for k, v in context.__dict__["_data"].items():
                res[k] = v
        else:
            logging.error("UE without context marshaled")
        res['uri'] = self.uri
        # rewrite assigned_accesspoint to URI
        res["assigned_accesspoint"] = self.assigned_accesspoint.uri if \
            self.assigned_accesspoint is not None else None
        return marshal(res, UE_RESOURCE_FIELDS)

    def assign_accesspoint(self, ap):
        """
        ATTENTION: Updates have to be atomic,
        to avoid record re-creation after previous delete.
        """
        try:
            UE.objects(uuid=self.uuid).update_one(
                set__assigned_accesspoint=ap)
            self.reload()
            assert(self.assigned_accesspoint == ap)
        except:
            # can fail if ue was deleted
            logging.warning("Assignment update failed.")

    def remove_accesspoint(self):
        """
        ATTENTION: Updates have to be atomic,
        to avoid record re-creation after previous delete.
        """
        try:
            UE.objects(uuid=self.uuid).update_one(
                set__assigned_accesspoint=None)
            self.reload()
            assert(self.assigned_accesspoint is None)
        except:
            # can fail if ue was deleted
            logging.warning("Assignment update failed.")

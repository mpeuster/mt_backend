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
    'active_application_package': fields.String,
    'active_application_activity': fields.String,
    'rx_total_bytes': fields.Integer,
    'tx_total_bytes': fields.Integer,
    'rx_mobile_bytes': fields.Integer,
    'tx_mobile_bytes': fields.Integer,
    'rx_wifi_bytes': fields.Integer,
    'tx_wifi_bytes': fields.Integer,
    'rx_total_bytes_per_second': fields.Float,
    'tx_total_bytes_per_second': fields.Float,
    'rx_mobile_bytes_per_second': fields.Float,
    'tx_mobile_bytes_per_second': fields.Float,
    'rx_wifi_bytes_per_second': fields.Float,
    'tx_wifi_bytes_per_second': fields.Float,
    'assigned_accesspoint': fields.String,
    'uri': fields.String,
    'wifi_mac': fields.String
}


class UE(Document):
    # system fields
    uuid = StringField(required=True, unique=True, primary_key=True)
    registered_at = DateTimeField(default=datetime.datetime.now)
    # user fields
    device_id = StringField(required=True, unique=True)
    location_service_id = StringField(default=None)
    wifi_mac = StringField(default=None)
    #####
    # system fields
    updated_at = DateTimeField(default=datetime.datetime.now)
    # user fields
    position_x = FloatField(default=-1)
    position_y = FloatField(default=-1)
    display_state = IntField(default=0)
    active_application_package = StringField(default=None)
    active_application_activity = StringField(default=None)
    rx_total_bytes = IntField(default=-1)
    tx_total_bytes = IntField(default=-1)
    rx_mobile_bytes = IntField(default=-1)
    tx_mobile_bytes = IntField(default=-1)
    rx_wifi_bytes = IntField(default=-1)
    tx_wifi_bytes = IntField(default=-1)
    rx_total_bytes_per_second = FloatField(default=-1)
    tx_total_bytes_per_second = FloatField(default=-1)
    rx_mobile_bytes_per_second = FloatField(default=-1)
    tx_mobile_bytes_per_second = FloatField(default=-1)
    rx_wifi_bytes_per_second = FloatField(default=-1)
    tx_wifi_bytes_per_second = FloatField(default=-1)
    # references
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
                set__wifi_mac=json_data["wifi_mac"],
                set__position_x=model.try_get(
                    json_data, "position_x", -1),
                set__position_y=model.try_get(
                    json_data, "position_y", -1),
                set__display_state=model.try_get(
                    json_data, "display_state", -1),
                set__active_application_package=model.try_get(
                    json_data, "active_application_package", None),
                set__active_application_activity=model.try_get(
                    json_data, "active_application_activity", None),
                set__rx_total_bytes=model.try_get(
                    json_data, "rx_total_bytes", -1),
                set__tx_total_bytes=model.try_get(
                    json_data, "tx_total_bytes", -1),
                set__rx_mobile_bytes=model.try_get(
                    json_data, "rx_mobile_bytes", -1),
                set__tx_mobile_bytes=model.try_get(
                    json_data, "tx_mobile_bytes", -1),
                set__rx_wifi_bytes=model.try_get(
                    json_data, "rx_wifi_bytes", -1),
                set__tx_wifi_bytes=model.try_get(
                    json_data, "tx_wifi_bytes", -1),
                set__rx_total_bytes_per_second=model.try_get(
                    json_data, "rx_total_bytes_per_second", -1),
                set__tx_total_bytes_per_second=model.try_get(
                    json_data, "tx_total_bytes_per_second", -1),
                set__rx_mobile_bytes_per_second=model.try_get(
                    json_data, "rx_mobile_bytes_per_second", -1),
                set__tx_mobile_bytes_per_second=model.try_get(
                    json_data, "tx_mobile_bytes_per_second", -1),
                set__rx_wifi_bytes_per_second=model.try_get(
                    json_data, "rx_wifi_bytes_per_second", -1),
                set__tx_wifi_bytes_per_second=model.try_get(
                    json_data, "tx_wifi_bytes_per_second", -1)
                )

            # try to use third party location if available
            try:
                loc = model.location.Location.objects.get(
                    location_service_id=json_data["location_service_id"])
                UE.objects(uuid=uuid).update_one(
                    set__position_x=loc.position_x,
                    set__position_y=loc.position_y)
                logging.debug("Used location service data with id: %s"
                              % json_data["location_service_id"])
            except:
                logging.debug("Could not find location info for %s."
                              % json_data["location_service_id"])
        except:
            logging.exception("Update error:")
            raise RequestError("Error during update.")

    @property
    def uri(self):
        return "%s/%s" % ("/api/ue", self.uuid)

    def marshal(self):
        """
        Builds the json representation of a UE.
        """
        res = {}
        # for k, v in self.__dict__["_data"].items():
        for k, v in self._data.items():
            res[k] = v
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
            logging.warning("Assignment update failed. (1)")

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
            logging.warning("Assignment update failed. (2)")

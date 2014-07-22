import logging
import datetime
import uuid
import model
from api.errors import *
from mongoengine import *
from flask.ext.restful import fields, marshal

AP_RESOURCE_FIELDS = {
    'uuid': fields.String,
    'device_id': fields.String,
    'location_service_id': fields.String,
    'registered_at': fields.DateTime,
    'ssid': fields.String,
    'position_x': fields.Float,
    'position_y': fields.Float,
    'power_state': fields.Integer,
    'assigned_ue_list': fields.List(fields.String),
    'uri': fields.String
}


class AccessPoint(Document):
    uuid = StringField(required=True, unique=True, primary_key=True)
    device_id = StringField(required=True, unique=True)
    location_service_id = StringField(required=True)
    registered_at = DateTimeField(default=datetime.datetime.now)
    ssid = StringField(default=None)
    position_x = FloatField(default=0)
    position_y = FloatField(default=0)
    power_state = IntField(default=0)  # 0=off, 1=on

    @staticmethod
    def create(json_data):
        try:
            ap = AccessPoint(
                uuid=uuid.uuid1().hex,
                device_id=json_data['device_id'],
                location_service_id=json_data['location_service_id'])
            ap.ssid = json_data['ssid']
            ap.position_x = json_data['position_x']
            ap.position_y = json_data['position_y']
            ap.save()
            logging.info("Registered AccessPoint: %s at %d/%d with SSID: %s" %
                         (ap.device_id, ap.position_x, ap.position_y, ap.ssid))
        except NotUniqueError:
            raise ResourceAlreadyExistsError("AP with this device_id exists.")
        except:
            logging.exception("Could not read AP config.")
            logging.info("Could not load config. Stopping daemon.")
            exit(1)
        return ap

    @staticmethod
    def get(uuid):
        try:
            ap = AccessPoint.objects.get(uuid=uuid)
        except:
            ap = None
        if ap is None:
            raise ResourceNotFoundError("AP not found in model.")
        return ap

    @staticmethod
    def load_from_config(json_list):
        for ap in json_list:
            AccessPoint.create(ap)

    @property
    def uri(self):
        return "%s/%s" % ("/api/accesspoint", self.uuid)

    def marshal(self):
        res = marshal(self.__dict__["_data"], AP_RESOURCE_FIELDS)
        res['assigned_ue_list'] = [ue.uri
                                   for ue in self.get_assigned_UE_list()]
        res['uri'] = self.uri
        return res

    def get_assigned_UE_list(self):
        return [ue for ue in model.ue.UE.objects
                if ue.assigned_accesspoint == self]

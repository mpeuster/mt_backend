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
    # 'psk': fields.String,
    'bssid': fields.String,
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
    psk = StringField(default=None)
    bssid = StringField(default=None)
    position_x = FloatField(default=0)
    position_y = FloatField(default=0)
    power_state = IntField(default=0)  # 0=off, 1=on

    @staticmethod
    def create(json_data):
        try:
            ap = AccessPoint(
                uuid=json_data['uuid'],  # uuid.uuid1().hex,
                device_id=json_data['device_id'],
                location_service_id=json_data['location_service_id'])
            ap.ssid = json_data['ssid']
            ap.psk = json_data['psk']
            ap.bssid = json_data['bssid']
            ap.position_x = json_data['position_x']
            ap.position_y = json_data['position_y']
            ap.power_state = json_data['power_state']
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
    def refresh(config_json, config_apmanger):
        """
        Deletes all existing access point objects from the database.

        Merges AP data from local config and from AP manager component.
        Both provided as argument with format dict.

        Only APs which are present in the manager AP list are used.
        Additional APs from the config are ignored. If an AP has no config
        entry, default values will be used for this.

        Attention: UUID from manager is also used locally.
        """
        # remove all old access point definitions
        model.accesspoint.AccessPoint.drop_collection()

        def find_ap(uuid):
            """
            Helper that finds APs from configuration file.
            Matching by either name or ssid.
            """
            for ap in config_json:
                if "uuid" in ap:
                    if ap["uuid"] == uuid:
                        return ap
            return None

        # merge AP info from manager and local config
        ap_lsit = []
        for apm in config_apmanger:  # only use AP definitions from manager
            if apm is not None:
                apc = find_ap(apm["uuid"])
                if apc is None:
                    # no config entry for AP found: use default values
                    logging.info("No local config for: %s" % apm["uuid"])
                    apc = {}
                    apc["device_id"] = apm["uuid"]
                    apc["location_service_id"] = apm["uuid"]
                    apc["ssid"] = "test"
                    apc["psk"] = None
                    apc["bssid"] = None
                    apc["position_x"] = 0
                    apc["position_y"] = 0
                # add manager values to config entry
                apc["uuid"] = apm["uuid"]
                apc["power_state"] = apm["power_state"]
                # finally create new AP from config entry
                AccessPoint.create(apc)

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

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
    'uri': fields.String,
    'serial': fields.String,
    'rx_bytes': fields.Integer,
    'tx_bytes': fields.Integer,
    'rx_bytes_per_second': fields.Float,
    'tx_bytes_per_second': fields.Float
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
    serial = StringField(default=None)
    rx_bytes = IntField(default=0)
    tx_bytes = IntField(default=0)
    rx_bytes_per_second = FloatField(default=0.0)
    tx_bytes_per_second = FloatField(default=0.0)
    last_stats_timestamp = FloatField(default=0.0)

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

    @staticmethod
    def update_info(uuid, ap_info):
        """
        Updates info data returned by the AP manager.
        """
        ap = AccessPoint.get(uuid)
        if ap is not None:
            if "name" in ap_info:
                ap.device_id = ap_info["name"]
            if "serial" in ap_info:
                ap.serial = ap_info["serial"]
            ap.save()

    @staticmethod
    def update_stats(uuid, ap_stats):
        """
        Updates and calculates network statistics returned
        by the AP manger.
        """
        ap = AccessPoint.get(uuid)
        if ap is not None:
            if "aps" in ap_stats:
                stats = ap.calculate_network_stats(ap_stats["aps"])
                # update model
                ap.rx_bytes = stats["rx_bytes"]
                ap.tx_bytes = stats["tx_bytes"]
                ap.rx_bytes_per_second = stats["rx_bytes_per_second"]
                ap.tx_bytes_per_second = stats["tx_bytes_per_second"]
                ap.last_stats_timestamp = stats["timestamp"]
                ap.save()
                logging.debug("AccessPoint %s: rx_bytes=%d tx_bytes=%d" %
                              (ap.device_id, ap.rx_bytes, ap.tx_bytes))

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

    def calculate_network_stats(self, stats_list):
        """
        Calculate and aggregate network states of all available
        radio interfaces of this access point.
        """
        new_timestamp = max([s["timestamp"] for s in stats_list])
        new_rx_bytes = sum([s["rxbyte"] for s in stats_list])
        new_tx_bytes = sum([s["txbyte"] for s in stats_list])
        new_rx_bytes_per_second = 0.0
        new_tx_bytes_per_second = 0.0

        if self.rx_bytes > 0:  # skip first run
            new_rx_bytes_per_second = (abs(new_rx_bytes - self.rx_bytes)
                                       / abs(new_timestamp
                                       - self.last_stats_timestamp))

        if self.tx_bytes > 0:  # skip first run
            new_tx_bytes_per_second = (abs(new_tx_bytes - self.tx_bytes)
                                       / abs(new_timestamp
                                       - self.last_stats_timestamp))

        # build result
        result = {
            "timestamp": new_timestamp,
            "rx_bytes": new_rx_bytes,
            "tx_bytes": new_tx_bytes,
            "rx_bytes_per_second": new_rx_bytes_per_second,
            "tx_bytes_per_second": new_tx_bytes_per_second
        }
        return result

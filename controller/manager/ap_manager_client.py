import requests
import json
import model
import logging
import urllib

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

RHEADER = {"content-type": "application/json"}


def get_connection():
    return ("http://%s:%d") % (model.CONFIG["apmanager"]["host"],
                               model.CONFIG["apmanager"]["port"])


def get_uuid_list(online_only=True):
    try:
        r = requests.get(
            get_connection() + "/api/network/accesspoint", headers=RHEADER)
        uuid_list = r.json()
        if online_only:
            return uuid_list["online"]
        else:
            return uuid_list["online"] + uuid_list["offline"]
    except:
        logging.error("Connection to AccessPointManager not possible.")
        return []


def get_accesspoint(uuid, include_power_state=False):
    try:
        r = requests.get(
            get_connection() + "/api/network/accesspoint/%s/info" % uuid,
            headers=RHEADER)
        ap = r.json()
        if include_power_state:
            r = requests.get(
                get_connection()
                + "/api/network/accesspoint/%s/power_state" % uuid,
                headers=RHEADER)
            ps = r.json()["power_state"]
            if ps == "radio_on":
                ap["power_state"] = 1
            else:
                ap["power_state"] = 0
        return ap
    except:
        logging.error("Connection to AccessPointManager not possible.")
        return None


def get_accesspoints():
    """
    Attention: Can return a list of None elements.
    """
    uuid_list = get_uuid_list()
    return [get_accesspoint(uuid, True) for uuid in uuid_list]


def set_power_state(uuid, power_state):
    try:
        if power_state:
            state = "radio_on"
        else:
            state = "radio_off"
        cmd = {"power_state": state}
        r = requests.put(
            get_connection() + "/api/network/accesspoint/"
            + uuid + "/power_state",
            data=json.dumps(cmd),
            headers=RHEADER)
        return r.status_code
    except:
        logging.exception("Connection to AccessPointManager not possible.")
        return None


def get_accesspoint_info(uuid):
    try:
        r = requests.get(
            get_connection()
            + "/api/network/accesspoint/%s/info" % uuid,
            headers=RHEADER)
        ap = r.json()
        return ap
    except:
        logging.error("Connection to AccessPointManager not possible.")
        return None


def get_accesspoint_stats(uuid):
    try:
        r = requests.get(
            get_connection()
            + "/api/network/accesspoint/%s/stats" % uuid,
            headers=RHEADER)
        ap = r.json()
        return ap
    except:
        logging.error("Connection to AccessPointManager not possible.")
        return None


def set_mac_list(mac, enable_on, disable_on):
    try:
        assert(isinstance(enable_on, list))
        assert(isinstance(disable_on, list))
        cmd = {}
        cmd["enable_on"] = enable_on
        cmd["disable_on"] = disable_on
        r = requests.put(
            get_connection() + "/api/network/client/" + urllib.quote_plus(mac),
            data=json.dumps(cmd),
            headers=RHEADER)
        logging.debug("Send mac list to AP manager for MAC: %s List: %s" % (mac, str(cmd)))
    except:
        logging.exception("Connection to AccessPointManager not possible.")
        return None

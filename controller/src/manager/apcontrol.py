import requests
import model
import logging


def get_connection():
    return ("http://%s:%d") % (model.CONFIG["apmanager"]["host"],
                               model.CONFIG["apmanager"]["port"])


def get_uuid_list(online_only=True):
    try:
        r = requests.get(get_connection() + "/api/network/accesspoint")
        uuid_list = r.json()
        if online_only:
            return uuid_list["online"]
        else:
            return uuid_list["online"] + uuid_list["offline"]
    except:
        logging.error("Connection to AccessPointManager not possible.")
        return []


def get_accesspoint(uuid):
    try:
        r = requests.get(
            get_connection() + "/api/network/accesspoint/%s" % uuid)
        ap = r.json()
        return ap
    except:
        logging.error("Connection to AccessPointManager not possible.")
        return None


def get_accesspoints():
    """
    Attention: Can return a list of None elements.
    """
    uuid_list = get_uuid_list()
    return [get_accesspoint(uuid) for uuid in uuid_list]

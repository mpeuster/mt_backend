import json
import logging
import accesspoint

"""
Configuration
"""
CONFIG = {}


def load_config(filename, basepath=""):
    global CONFIG
    try:
        json_file = open(basepath + filename)
        CONFIG = json.load(json_file)
        json_file.close()
        logging.info("Using configuration file: %s%s" % (basepath, filename))
    except:
        logging.exception(
            "Can not load config file: %s%s. " % (basepath, filename))
        logging.info("Could not load config. Stopping daemon.")
        exit(1)

"""
AccessPoint Management
"""
AccessPoints = {}


def load_aps_from_config(data):
    for ap in data:
        new = accesspoint.AccessPoint(
            ap["name"],
            ap["ssid"],
            ap["state"]
            )
        add_ap(new)
        logging.info("Added AP: %s" % str(new))


def add_ap(ap):
    if ap.uuid in AccessPoints:
        logging.error("AP with UUID already exists in model.")
        return
    AccessPoints[ap.uuid] = ap


def remove_ap(ap):
    if ap.uuid not in AccessPoints:
        logging.error("AP with UUID not in model.")
        return
    del AccessPoints[ap.uuid]

"""
Helper
"""


def try_get(data, key, default=None):
    """
    Tries to get the key from the dict, or
    returns default value.
    """
    if key not in data:
        return default
    return data[key]

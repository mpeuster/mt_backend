import json
import logging
import mongoengine
from ue import UE
from location import Location
from accesspoint import AccessPoint


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
        logging.info("Stopping daemon.")
        exit(1)

"""
Database
"""


def coonect_db():
    # connect to mongodb
    # TODO: Extended DB setup and logging
    mongoengine.connect(CONFIG["database"]["db"])
    # clear db
    UE.drop_collection()
    Location.drop_collection()
    AccessPoint.drop_collection()

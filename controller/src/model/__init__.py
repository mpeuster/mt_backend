import json
import logging
import mongoengine
import location
import accesspoint
import ue

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
Database
"""


def connect_db():
    # connect to mongodb
    try:
        mongoengine.connect(
            CONFIG["database"]["db"],
            host=CONFIG["database"]["host"],
            port=CONFIG["database"]["port"],
            username=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"]
            )
        # clear db
        ue.UE.drop_collection()
        location.Location.drop_collection()
        accesspoint.AccessPoint.drop_collection()
        logging.info("Connected to MongoDB: %s@%s:%d"
                     % (CONFIG["database"]["db"],
                        CONFIG["database"]["host"],
                        CONFIG["database"]["port"]))
    except:
        logging.exception("Could not connect to database")
        logging.info("Database connection failed. Stopping daemon.")

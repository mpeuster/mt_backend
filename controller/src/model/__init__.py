import logging
import mongoengine
from ue import UE
from location import Location


def coonect_db():
    # connect to mongodb
    # TODO: move this to config file
    mongoengine.connect("test")
    # clear db
    UE.drop_collection()
    Location.drop_collection()


def get_instance():
    return SystemModel.get_instance()


class SystemModel(object):
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = SystemModel()
            logging.info("SystemModel instance created: %s"
                         % str(cls._INSTANCE))
        return cls._INSTANCE

    def __init__(self):
        if self._INSTANCE is not None:
            raise ValueError("An instance of the system model already exists.")

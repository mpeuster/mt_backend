import logging
from model.ue import *
from api.errors import ResourceAlreadyExistsError, ResourceNotFoundError
import mongoengine
import uuid


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
        # connect to mongodb
        # TODO: move this to config file
        mongoengine.connect("test")
        # clear db
        UE.drop_collection()

    """
        self._ue_dict = {}
        self.ap_list = []

    def create_ue(self, json_data):
        new_ue = model.ue.UE(json_data)
        if new_ue.uuid in self._ue_dict:
            raise ResourceAlreadyExistsError("UE already exists in model.")
        if new_ue.device_id in [ue.device_id for ue in
                                self._ue_dict.itervalues()]:
            raise ResourceAlreadyExistsError("UE with this device_id exists.")
        self._ue_dict[new_ue.uuid] = new_ue
        return new_ue

    def get_ue(self, uuid):
        if uuid in self._ue_dict:
            return self._ue_dict[uuid]
        raise ResourceNotFoundError("UE not found in model.")

    def get_ue_dict(self):
        return self._ue_dict

    """

    # TODO: maybe move to UE class as static method
    def create_ue(self, json_data):
        try:
            new_ue = UE(uuid=uuid.uuid1().hex,
                        device_id=json_data['device_id'])
            new_ue.update_with_json(json_data)
            new_ue.add_context(json_data)
            new_ue.save()
        except NotUniqueError:
            raise ResourceAlreadyExistsError("UE with this device_id exists.")
        except:
            pass  # TODO: raise DB Exception
        return new_ue

    def update_ue(self, uuid, json_data):
        ue = self.get_ue(uuid)
        ue.update_with_json(json_data)
        ue.add_context(json_data)
        ue.save()

    def delete_ue(self, uuid):
        ue = self.get_ue(uuid)
        ue.delete()

    def get_ue(self, uuid):
        try:
            ue = UE.objects.get(uuid=uuid)
        except:
            ue = None
        if ue is None:
            raise ResourceNotFoundError("UE not found in model.")
        return ue

    def get_ue_dict(self):
        res = {}
        for ue in UE.objects:
            res[ue.uuid] = ue
        return res

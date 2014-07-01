import logging
import model.ue
from api.errors import *

class SystemModel(object):
	_INSTANCE = None

	@classmethod
	def get_instance(cls):
		if cls._INSTANCE is None:
			cls._INSTANCE = SystemModel()
			logging.info("SystemModel instance created: %s" % str(cls._INSTANCE))
		return cls._INSTANCE

	def __init__(self):
		if self._INSTANCE is not None:
			raise ValueError("An instance of the system model already exists.")

		self._ue_dict = {}
		self.ap_list = []

	def create_ue(self, json_data):
		new_ue = model.ue.UE(json_data)
		if new_ue.uuid in self._ue_dict:
			raise ResourceAlreadyExistsError("UE already exists in model.")
		self._ue_dict[new_ue.uuid] = new_ue
		return new_ue

	def get_ue(self, uuid):
		if uuid in self._ue_dict:
			return self._ue_dict[uuid]
		raise ResourceNotFoundError("UE not found in model.")

	def get_ue_dict(self):
		return self._ue_dict
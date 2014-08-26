import logging
import datetime
import uuid
from mongoengine import *


class Location(Document):
    """
    This is only used to store values of the third party location service.

    ATTENTION:
    These values are only pulled to the UE context model, when an UE context
    update is performed!
    """
    location_service_id = StringField(required=True, unique=True,
                                      primary_key=True)
    position_x = FloatField(default=0)
    position_y = FloatField(default=0)

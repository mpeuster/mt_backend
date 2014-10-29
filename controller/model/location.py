import logging
import datetime
import uuid
from mongoengine import *


class Location(Document):
    """
    This is only used to store values of the third party location service.
    """
    location_service_id = StringField(required=True, unique=True,
                                      primary_key=True)
    position_x = FloatField(default=0)
    position_y = FloatField(default=0)

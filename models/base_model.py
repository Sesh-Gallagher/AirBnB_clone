#!/usr/bin/python3
"""Module for the base model script"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """Represents class from which all other classes will inherit"""


def __init__(self, *args, **kwargs):
    """initializes attributes of an instance

    Args:
     - *args: the list of arguments
     - **kwargs: dict of key-values and args."""

    if kwargs is not None and kwargs != {}:
        for key in kwargs:
            if key == "created_at":
                self.__dict__["created_at"] = datetime.strptime(
                         kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            elif key == "updated_at":
                self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.__dict__[key] = kwargs[key]
    else:
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        storage.new(self)


def __str__(self):
    """Module returns official string representation"""

    return "[{}] ({}) {}".\
        format(type(self).__name__, self.id, self.__dict__)


def save(self):
    """Module updates the public instance attribute updated_at"""

    self.updated_at = datetime.now()
    storage.save()


def to_dict(self):
    """Module returns a dictionary containing all keys/values of __dict__"""

    my_dict = self.__dict__.copy()
    my_dict["__class__"] = type(self).__name__
    my_dict["created_at"] =
    my_dict["created_at"].isoformat()
    my_dict["updated_at"] =
    my_dict["updated_at"].isoformat()
    return my_dict

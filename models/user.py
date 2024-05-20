#!/usr/bin/python3
"""Module that creates a User class"""

from models.base_model import BaseModel


class User(BaseModel):
    """Represents a class for managing user objects"""

    first_name = ""
    last_name = ""
    passsword = ""
    email = ""

#!/usr/bin/python3
"""Module that creates a review class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Represents class for managing review objects"""

    text = ""
    user_id = ""
    place_id = ""

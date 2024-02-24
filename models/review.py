#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """This is the class for Review

    Attributes:
        place_id: (sqlalchemy String): Review's place id.
        user_id: (sqlalchemy String): Review's place id.
        text: (sqlalchemy String): Review description
    """

    __tablename__ = "reviews"

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        place_id = ''
        user_id = ''
        text = ''

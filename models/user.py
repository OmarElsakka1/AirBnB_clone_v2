#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ Handling User class in MySQL database.

    Attributes:
        __tablename__: for the table name, users
        email: (sqlalchemy String): User's email address.
        password (sqlalchemy String): User's password.
        first_name (sqlalchemy String): User's first name.
        last_name (sqlalchemy String): User's last name.
        places (sqlalchemy relationship): User&Place relationship.
        reviews (sqlalchemy relationship): User&Review relationship.

    """

    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship('Place', backref='user',  cascade='delete')
    reviews = relationship('Review', backref='user',  cascade='delete')

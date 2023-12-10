#!/usr/bin/python3
"""
 Module for class User
"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    class User inherits from Basemodel
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""

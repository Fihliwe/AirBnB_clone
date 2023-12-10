#!/usr/bin/python3
'''
This Module contains the BaseModel class
'''
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    '''
    This class defines all common attributes/methods for the other classes
    '''
    def __int__(self, *args, **kwargs):
        '''
        initializes all public instance attributes of the BaseModel class
        Args:
            *args : unused.
            **kwargs(dict) : key/value pairs of attributes. 
        '''
        TimeFormat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        created_at = datetime.today()
        updated_at = datetime.today()

        if len(kwargs) != 0:
            for i, j in kwargs.items():
                if i == "created-at" or j == "updated_at":
                    self.__dict__[i] = datetime.strptime(j, TimeFormat)
                else:
                    self.__dict__[i] = j
        else:
            models.storage.new(self)

    def save(self):
        '''
        updates the public instance attribute updated_at with the current datetime
        '''
        self.updated_at = datetime.today()
        models.storage.save()
        

    def to_dict(self):
        '''
        returns a dictionary containing all key/values
        '''
        bdict = self.__dict__.copy()
        bdict["created_at"] = self.created_at.isoformat()
        bdict["updated_at"] = self.updated_at.isoformat()
        bdict["__class__"] = self.__class__.__name__
        return bdict

    def __str__(self):
        '''
        should print: [<class name>] (<self.id>) <self.__dict__>
        '''
        strname = self.__class__.__name__
        return "[{}] ({}) {}".format(strname,self.id, self.__dict__)

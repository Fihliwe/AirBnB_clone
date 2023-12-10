#!/usr/bin/python3
"""
This is a module for FileStorage class which serializes insatnces to 
a JSON file and deserializes JSON file to instances
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    serializes insatnces to 
    a JSON file and deserializes JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        returns the dictionary __objects
        """
        return FileStorage.__objects
    
    def new(self, obj):
        """
        sets objects in the obj
        """
        objectname = obj.__class__.__name__
        FileStorage.__objects[f"{objectname}.{obj.id}"] = obj

    def save(self):
        """
        serializes objects to the JSON file path
        """
        objectdict = FileStorage.__objects
        obdict = {obj: objectdict[obj].to_dict for obj in objectdict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(obdict, f)

        def reload(self):
            """
             deserializes the JSON file to __objects (only if the JSON file 
             (__file_path) exists ; otherwise, do nothing. If the file doesn’t
            exist, no exception should be raised)
            """
            try:
                with open(FileStorage.__file_path) as f:
                    obdict = json.load(f)
                    for o in obdict.values():
                        cls_name = o["__class__"]
                        del o["__class__"]
                        self.new(eval(cls_name)(**o))
            except FileNotFoundError:
                return

#!/usr/bin/pyhton3
"""
contains the entry point of the command interpreter:
"""
import cmd
import re
from shlex import split
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """
    parse's arguements into the code syntax
    """
    c_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if c_braces is None:
        if brackets  is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            ret1 = [i.strip(",") for i in lexer]
            ret1.append(brackets.group())
            return ret1
    else:
        lexer = split(arg[:c_braces.span()[0]])
        ret1 = [i.strip(",") for i in lexer]
        ret1.append(c_braces.group())
        return ret1

class HBNBCommand(cmd.Cmd):
    """
    class definition
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def default():
        """
        default behaviour for cmd module when input is invalid
        """
    
    def do_quit(self, arg):
        """
        quit command to exit line interpreter
        """
        return True
    
    def do_EOF(self, arg):
        """
        end-of-line command to exit the line interpreter
        """
        print("")
        return True
    
    def emptyline(self, arg):
        """
        doesnt execute anything
        """
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file)
        """
        arg1 = parse(arg)
        if len(arg1) == 0:
            print("** class name missing **")
        elif arg1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg1[0]().id))
            storage.save()

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on the class 
        name and id.
        """
        arg1 = parse(arg)
        objectdict = storage.all()
        if len(arg1) == 0:
            print("** class name missing **")
        elif arg1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg1) == 1:
            print("** instance id missing **")
        elif "f{arg1[0]}.{arg1[1]}" not in objectdict:
            print("** no instance found **")
        else:
            print(objectdict[f"{arg1[0]}.{arg[1]}"])

    def do_destroy(self, arg):
        """
         Deletes an instance based on the class name and id
        """
        arg1 = parse(arg)
        objectdict = storage.all()
        if len(arg1) == 0:
            print("** class name missing **")
        elif arg1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg1) == 1:
            print("** instance id missing **")
        elif "f{arg1[0]}.{arg1[1]}" not in objectdict.keys():
            print("** no instance found **")
        else:
            del objectdict[f"{arg1[0]}.{arg[1]}"]
            storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not on the
        class name
        """
        arg1 = parse(arg)
        if len(arg1) > 0 and arg1[0] not in HBNBCommand.__classes:
            print("** class doesnt exits **")
        else:
            obj1 = []
            for obj in storage.all().values():
                if len(arg1) > 0 and arg1[0] == obj.__class__.__name__:
                    count += 1
            print(count)

    def do_update(self, arg):
        """
         Updates an instance based on the class name and id by adding 
         or updating attribute (save the change into the JSON file). 
        """
        arg1 = parse(arg)
        objectdict = storage.all()

        if len(arg1) == 0:
            print("** class name missing **")
            return False
        if arg1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg1) == 1:
            print("** instance id missing **")
            return False
        if  "{}.{}".format(arg1[0], arg1[1]) not in objectdict.keys():
            print("** no instance found **")
            return False
        if len(arg1) == 2:
            print("** attribute name missing **")
            return False
        if len(arg1) == 3:
            try:
                type(eval(arg1[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg1) == 4:
            obj = objectdict["{}.{}".format(arg1[0], arg1[1])]
            if arg1[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg1[2]])
                obj.__dict__[arg1[2]] = valtype(arg1[3])
            else:
                obj.__dict__[arg1[2]] = arg1[3]
        elif type(eval(arg1[2])) == dict:
            obj = objectdict["{}.{}".format(arg1[0], arg1[1])]
            for k, v in eval(arg1[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

if __name__ == "__main__":
    HBNBCommand().cmdloop()

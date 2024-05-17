#!/usr/bin/python3
"""Represents module for the entry point of CMD interpreter."""

import re
import json
import cmd
from models.base_model import BaseModel
from models import storage


class HBNBCommand (cmd.cmd):
    """Represents class for CMD interpreter."""

    prompt = "(hbnb) "

    def default(self, line):
        """Receives command and if no match then. """
        # print("DEF:::", line)
        self._precmd(line)

    def _precmd(self, line):
        """checks commands to test class.sytaxx()"""
        # print("PRECMD:::", line)
        match = re.search(r"^(\w*)\.(\w+(?:\(([^)]*)\))$", line)

        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                    '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(1) or "") + " " +
    (match_attr_and_value.group(2) or "")
    command = method + " " + classname + " " + uid + " " + attr_and_value
    self.onecmd(command)
    return command

    def update_dict(self, classname, uid, s_dict):
        """Helps method for update() with a dict."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class does not exist **")
        elif uid is None:
            print("** instance id is missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** instance not found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_EOF(self, line):
        """Checks end of file character."""
        print()
        return True

    def do_quit(self, line):
        """Exits the program."""
        return True

    def emptyline(self):
        """inactive on enter."""
        pass

    def do_create(self, line):
        """ Starts and creates an instance."""
        if line == "" or line is None:
            print("** clase name is missing **")
        elif line not in storage.classes():
            print("** class does not exist **")
        else:
            b = storage.classes()[line]()
            b.save()
            print(b.id)

    def do_show(self, line):
        """Prints the string represented in the instance."""
        if line == "" or line is None:
            print("** class name cannot be found **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class does not exit **")
            elif len(words) < 2:
                print("** instance id is missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance has been found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes instance based on class name and id."""
        if line == "" or line is None:
            print("** class name is missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class does not exist **")
            elif len(words) < 2:
                print("** instance id cannot be found **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** instance cannot be found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        """Prints string representation of all instances."""
        if line != "":
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class does not exist **")
            else:
                nl = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == words[0]]
                print(nl)
            else:
                new_list = [str(obj) for key, obj in storage.all().items()]
                print(new_list)

    def do_count(self, line):
        """ Counts instances of/in a class."""
    words = line.split(' ')
    if not words[0]:
        print("**class name is not found**")
    elif words[0] not in storage.classes():
        print("** class does not exist **")
    else:
        matches = [a for a in storage.all() if a.startswith(words[0] + '.')]
        print(len(matches))

    def do_update(self, line):
        """update the instance by adding or updating attributes."""
        if line == "" or line is None:
            print("** class name cannot be found **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name cannot be found **")
        elif classname not in storage.classes():
            print("** class does not exist **")
        elif uid is None:
            print("** instance id cannot be found **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** instance cannot be found **")
            elif not attribute:
                print("** attribute name cannot be found **")
            elif not value:
                print("** value cannot be found **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attribute()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                    setattr(storage.all()[key], attribute, value)
                    storage.all()[key].save()

    if __name__ == '__main__':
        HBNBCommand().cmdloop()

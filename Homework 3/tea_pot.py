import json
from pathlib import Path
import errors

class TeaPot(object):
    """Represents a teapot"""

    pot_type = "tea"

    def __init__(self, pot_designator, additions, tea_type):
        self.pot_designator = pot_designator
        self.additions = additions
        self.tea_type = tea_type
        self.create_pot_file()

    
    def create_pot_file(self):
        """Creates the file of the json description, raising an error if the file already exists"""
        tea_file = Path("{}/{}".format(self.pot_designator, self.tea_type))
        tea_directory = Path(self.pot_designator)

        if tea_file.exists():
            raise errors.PotExists
        
        try:
            tea_directory.mkdir()
        except FileExistsError:
            raise errors.PotExists
        
        with tea_file.open(mode='w') as f:
            json.dump(self.as_dict(), f, indent=4)


    def as_dict(self):
        """Returns the tea pot in dictonary form"""
        tea_dict = dict()
        tea_dict["type"] = "tea"
        tea_dict["variety"] = self.tea_type
        tea_dict["Additions"] = dict()
        for counter, addition in enumerate(self.additions, 1):
            addition_key = "addition{}".format(counter)
            tea_dict["Additions"][addition_key] = addition
        
        return tea_dict

    def __str__(self):
        return "/{}/{}".format(self.pot_designator, self.tea_type)
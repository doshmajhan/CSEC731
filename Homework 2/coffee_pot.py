import json
import os
from pathlib import Path
import errors


class CoffeePot(object):
    """Represents a coffee pot"""

    pot_type = "coffee"

    def __init__(self, pot_designator, additions):
        self.pot_designator = pot_designator
        self.additions = additions
        self.create_pot_file()
    
    def create_pot_file(self):
        """Creates the file of the json description, raising an error if the file already exists"""
        coffee_file = Path(self.pot_designator)

        if coffee_file.exists():
            raise errors.PotExists
        
        with coffee_file.open(mode='w') as f:
            json.dump(self.as_dict(), f, indent=4)


    def as_dict(self):
        """Returns the coffee pot in dictonary form"""
        coffee_dict = dict()
        coffee_dict["type"] = "coffee"
        coffee_dict["Additions"] = dict()
        for counter, addition in enumerate(self.additions, 1):
            addition_key = "addition{}".format(counter)
            coffee_dict["Additions"][addition_key] = addition
        
        return coffee_dict
        
    def __str__(self):
        return "/{}".format(self.pot_designator)

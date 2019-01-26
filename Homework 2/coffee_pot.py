import json
import os
from pathlib import Path
import errors


class CoffeePot(object):
    """Represents a coffee pot"""

    def __init__(self, pot_number, uri, additions):
        self.pot_number = pot_number
        self.uri = uri
        self.additions = additions
        self.type = "coffee"
    
    def create_pot_file(self):
        """Creates the file of the json description, raising an error if the file already exists"""
        # trim off the leading slash
        coffee_file = Path(self.uri[1:])

        if coffee_file.exists():
            raise errors.PotExists
        
        with coffee_file.open() as f:
            json.dump(self.as_dict(), f)


    def as_dict(self):
        """Returns the coffee pot in dictonary form"""
        coffee_dict = dict()
        coffee_dict["type"] = "coffee"
        coffee_dict["Additions"] = dict()
        for counter, addition in enumerate(self.additions, 1):
            addition_key = "addition{}".format(counter)
            coffee_dict["Additions"][addition_key] = addition
        
        return coffee_dict
        

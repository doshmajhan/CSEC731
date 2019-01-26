class TeaPot(object):
    """Represents a teapot"""

    def __init__(self, pot_number, uri, additions):
        self.pot_number = pot_number
        self.uri = uri
        self.additions = additions
        self.type = "tea"
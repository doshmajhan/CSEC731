"""
    Possible errors to be thrown when parsing requests
"""

class InvalidRequestLine(Exception):
    pass

class UnsupportedMethod(Exception):
    pass

class InvalidVersion(Exception):
    pass

class InvalidURI(Exception):
    pass
"""
    Possible errors to be thrown when parsing requests
"""

##########################
# General request errors #
##########################

class RequestError(Exception):
    def __init__(self):
        self.message = None
        self.code = None
        self.reason_phrase = None

class InvalidHeader(RequestError):
    def __init__(self):
        self.message = "Invalid header"
        self.code = 400
        self.reason_phrase = "Bad Request"

class UnsupportedMethod(RequestError):
    def __init__(self):
        self.message = "Unsupported Method"
        self.code = 405
        self.reason_phrase = "Method Not Allowed"

class InvalidURI(RequestError):
    def __init__(self):
        self.message = "Invalid URI"
        self.code = 400
        self.reason_phrase = "Bad Request"

class InvalidContentType(RequestError):
    def __init__(self):
        self.message = "Invalid content type"
        self.code = 400
        self.reason_phrase = "Bad Request"

class InvalidVersion(RequestError):
    def __init__(self):
        self.message = "Invalid version"
        self.code = 400
        self.reason_phrase = "Bad Request"

#########################
# HTCPCP specifc errors #
#########################

class HTCPCPError(RequestError):
    def __init__(self):
        self.message = None
        self.code = None
        self.reason_phrase = None

class UnsupportedTeaType(HTCPCPError):
    def __init__(self):
        self.message = "Unsupported tea type"
        self.code = 403
        self.reason_phrase = "Forbidden"

class UnsupportedAdditions(HTCPCPError):
    def __init__(self):
        self.message = "Unsupported addition"
        self.code = 403
        self.reason_phrase = "Forbidden"

class ImATeapotError(HTCPCPError):
    def __init__(self):
        self.message = "I'm a teapot"
        self.code = 418
        self.reason_phrase = "I'm a teapot"

class PotExists(HTCPCPError):
    def __init__(self):
        self.message = "Pot already exists"
        self.code = 403
        self.reason_phrase = "Forbidden"

class BrewNotStarted(HTCPCPError):
    def __init__(self):
        self.message = "Brewing for this pot has not started"
        self.code = 404
        self.reason_phrase = "Not Found"

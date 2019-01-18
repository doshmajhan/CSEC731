"""
    Possible errors to be thrown when parsing requests
"""
class HTCPCPException(Exception):
    def __init__(self):
        self.message = None
        self.code = None

class InvalidRequestLine(HTCPCPException):
    def __init__(self):
        self.message = "Invalid request line"
        self.code = 400

class InvalidVersion(HTCPCPException):
    def __init__(self):
        self.message = "Invalid version"
        self.code = 400

class InvalidURI(HTCPCPException):
    def __init__(self):
        self.message = "Invalid URI"
        self.code = 400

class InvalidHeader(HTCPCPException):
    def __init__(self):
        self.message = "Invalid header"
        self.code = 400

class InvalidContentType(HTCPCPException):
    def __init__(self):
        self.message = "Invalid content type"
        self.code = 400

class UnsupportedTeaType(HTCPCPException):
    def __init__(self):
        self.message = "Unsupported tea type"
        self.code = 403

class UnsupportedAdditions(HTCPCPException):
    def __init__(self):
        self.message = "Unsupported addition"
        self.code = 403

class UnsupportedMethod(HTCPCPException):
    def __init__(self):
        self.message = "Unsupported method"
        self.code = 403

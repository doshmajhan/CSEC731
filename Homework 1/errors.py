"""
    Possible errors to be thrown when parsing requests
"""
class HTCPCPException(Exception):
    def __init__(self):
        self.message = None
        self.code = None
        self.reason_phrase = None

class InvalidRequestLine(HTCPCPException):
    def __init__(self):
        self.message = "Invalid request line"
        self.code = 400
        self.reason_phrase = "Bad Request"

class InvalidVersion(HTCPCPException):
    def __init__(self):
        self.message = "Invalid version"
        self.code = 400
        self.reason_phrase = "Bad Request"

class InvalidURI(HTCPCPException):
    def __init__(self):
        self.message = "Invalid URI"
        self.code = 400
        self.reason_phrase = "Bad Request"

class InvalidHeader(HTCPCPException):
    def __init__(self):
        self.message = "Invalid header"
        self.code = 400
        self.reason_phrase = "Bad Request"

class InvalidContentType(HTCPCPException):
    def __init__(self):
        self.message = "Invalid content type"
        self.code = 400
        self.reason_phrase = "Bad Request"

class UnsupportedTeaType(HTCPCPException):
    def __init__(self):
        self.message = "Unsupported tea type"
        self.code = 403
        self.reason_phrase = "Forbidden"

class UnsupportedAdditions(HTCPCPException):
    def __init__(self):
        self.message = "Unsupported addition"
        self.code = 403
        self.reason_phrase = "Forbidden"

class UnsupportedMethod(HTCPCPException):
    def __init__(self):
        self.message = "Unsupported method"
        self.code = 403
        self.reason_phrase = "Forbidden"

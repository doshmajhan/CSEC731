import errors

VALID_METHODS = ['GET', 'BREW', 'POST', 'WHEN', 'PROPFIND']
VALID_VERSION = "HTCPCP-TEA/1.0"
VALID_CONTENT_TYPES = {
    "coffee": "message/coffee-pot-command",
    "tea": "message/teapot"
}
VALID_ADDITIONS = [
    "cream", "half-and-half", "whole-milk", 
    "part-Skim", "skim", "non-Dairy",
    "vanilla", "almond", "raspberry",
    "chocolate", "whisky", "rum",
    "kahlua", "aquavit", "sugar",
    "xylitol", "stevia", "*"
]
VALID_TEA_TYPES = ["peppermint", "black", "green", "earl-grey"]

class HTCPCPRequest(object):
    """
    Class to hold a HTCPCP request
    """

    def __init__(self, request_line, headers, body):
        self.validate_request_line(request_line)
        self.headers = self.validate_headers(headers)
        self.body = body

    def validate_request_line(self, request_line):

        try:
            method, uri, version = request_line.split()
        except ValueError:
            raise errors.InvalidURI

        self.method = self.validate_method(method)
        self.uri = self.validate_uri(uri)
        self.version = self.validate_version(version)

    def validate_method(self, method):

        if method not in VALID_METHODS:
            raise errors.UnsupportedMethod

        return method

    def validate_uri(self, uri):
        
        if uri.count("/") == 0:
            raise errors.InvalidURI

        if uri == "/":
            return uri

        if uri.count("?") > 0:
            uri, additions = uri.split("?", 1)
            self.validate_additions(additions.split("&"))
        
        parts = uri.split("/")
        pot = parts[1]
        self.pot_number = self.validate_pot(pot)

        if len(parts) > 2:
            self.type = "tea"
            self.tea_type = parts[2]
            if self.tea_type not in VALID_TEA_TYPES:
                raise errors.UnsupportedTeaType

        else:
            self.type = "coffee"

        return uri

    def validate_pot(self, pot_designator):
        if pot_designator.count("-") != 1:
            raise errors.InvalidURI

        parts = pot_designator.split("-")
        if parts[0] != "pot":
            raise errors.InvalidURI
        
        try:
            pot_number = int(parts[1])
        except ValueError:
            raise errors.InvalidURI
        
        return pot_number

    def validate_version(self, version):
        if version != VALID_VERSION:
            raise errors.InvalidVersion

        return version

    def validate_headers(self, headers):
        header_dict = dict()

        for header in headers:
            try:
                name, value = header.split(":")
                value = value.strip()
            except ValueError:
                raise errors.InvalidHeader
            
            if name == "Content-Type":
                header_dict[name] = self.validate_content_type(value)

            if name == "Accept-Additions":
                additions = [a.strip() for a in value.split(";")]
                header_dict[name] = self.validate_additions(additions)

        return header_dict
    
    def validate_content_type(self, content_type):
        if self.uri == "/":
            pass
        elif content_type != VALID_CONTENT_TYPES[self.type]:
            if self.type == "tea" and content_type == VALID_CONTENT_TYPES["coffee"]:
                raise errors.ImATeapotError

            raise errors.InvalidContentType
        
        return content_type

    def validate_additions(self, additions):
        for a in additions:
            if a.lower() not in VALID_ADDITIONS:
                raise errors.UnsupportedAdditions

        self.additions = additions
        return additions
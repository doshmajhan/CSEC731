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

    Attributes:
        request_line (string): the request line containing the request method, uri and version
        headers (dict): a dictionary containing the header names and associated values
        body (string): the body of the request
    """

    def __init__(self, request_line, headers, body):
        self.additions = list()
        self.validate_request_line(request_line)
        self.headers = self.validate_headers(headers)
        self.body = body

    def validate_request_line(self, request_line):
        """
        Validates that the request line has a supported method, a correct uri and correct version

        Parameters:
            request_line (string): the request line of the request
        """
        self.request_line = request_line
        
        try:
            method, uri, version = request_line.split()
        except ValueError:
            raise errors.InvalidURI

        self.method = self.validate_method(method)
        self.uri = self.validate_uri(uri)
        self.version = self.validate_version(version)

    def validate_method(self, method):
        """
        Validates that the method is in the list of VALID_METHODS

        Parameters:
            method (string): the request method contained in the request line
        
        Returns:
            method (string): the validated method
        """
        if method not in VALID_METHODS:
            raise errors.UnsupportedMethod

        # temporary for this assignment
        if method == "POST":
            raise errors.InvalidRequestLine

        return method

    def validate_uri(self, uri):
        """
        Validates that the URI follows the RFC, having a correct pot designator, valid additions
        if they are being passed through the URI and valid tea type if it is for a tea pot

        Parameters:
            uri (string): the URI from the request line
        
        Returns:
            uri (string the uri if it has been deemed valid
        """
        if uri.count("/") == 0:
            raise errors.InvalidURI

        if uri == "/":
            return uri

        if uri.count("?") > 0:
            uri, additions = uri.split("?", 1)
            self.validate_additions(additions.split("&"))
        
        parts = uri.split("/")
        pot = parts[1]
        self.pot_designator = self.validate_pot(pot)

        if len(parts) > 2:
            self.type = "tea"
            self.tea_type = parts[2]
            if self.tea_type not in VALID_TEA_TYPES:
                raise errors.UnsupportedTeaType

        else:
            self.type = "coffee"

        return uri

    def validate_pot(self, pot_designator):
        """
        Validate the the pot designator format is correct(ex: pot-1)

        Parameters:
            pot_designator (string): the post designator contained within the URI

        Returns:
            pot_designator (string): the validated post designator contained within the URI
        """
        if pot_designator.count("-") != 1:
            raise errors.InvalidURI

        parts = pot_designator.split("-")
        if parts[0] != "pot":
            raise errors.InvalidURI
        
        try:
            pot_number = int(parts[1])
        except ValueError:
            raise errors.InvalidURI
        
        return pot_designator

    def validate_version(self, version):
        """
        Validates the version is supported

        Parameters:
            version (string): the version contained within the request line

        Returns:
            version (string): the validated version
        """
        if version != VALID_VERSION:
            raise errors.InvalidVersion

        return version

    def validate_headers(self, headers):
        """
        Validates the headers are in the correct format

        Paremeters:
            headers (list): a list of parsed header strings

        Returns:
            header_dict (dict): a dictionary with header names and their values
        """
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
        """
        Validates that the value in the content type matches up with the type determined from the URI

        Parameters:
            content_type (string): the content type value parsed from the header string

        Returns:
            content_type (string): the validated content type
        """
        if self.uri == "/":
            return content_type

        if content_type != VALID_CONTENT_TYPES[self.type]:
            if self.type == "tea" and content_type == VALID_CONTENT_TYPES["coffee"]:
                raise errors.ImATeapotError

            raise errors.InvalidContentType
        
        return content_type

    def validate_additions(self, additions):
        """
        Validates that each addition submitted through query parameters or
        the Accept-Additions header is supported

        Parameters:
            additions (list): a list strings of additions that was parsed from the request

        Returns:
            addtions (list): the list of validated additions
        """
        for a in additions:
            if a.lower() not in VALID_ADDITIONS:
                raise errors.UnsupportedAdditions
            
            self.additions.append(a)
        
        return additions
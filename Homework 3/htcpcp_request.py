from collections import Counter
import errors
from coffee_pot import CoffeePot
from tea_pot import TeaPot
from response import Response


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
BREWING_POTS = list()

class HTCPCPRequest(object):
    """
    Class to hold a HTCPCP request

    Attributes:
        request_line (string): the request line containing the request method, uri and version
        headers (dict): a dictionary containing the header names and associated values
        body (string): the body of the request
    """

    def __init__(self, request):
        """
        Parameters:
            request (Request): a request object containing the parsed HTCPCP request
        """
        self.method = self.validate_method(request.method)
        self.uri = self.validate_uri(request.uri)
        self.headers = request.headers
        self.body = request.body
        self.content_type = self.validate_content_type(request.content_type)

        if request.query_string and self.method == "GET":
            self.additions = self.validate_additions(request.query_string)
        elif request.method == "BREW":
            additions = [a.strip() for a in self.headers["Accept-Additions"].split(";")]
            self.additions = self.validate_additions(additions)
            

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
        if uri == "/":
            return uri
        
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
        
        return additions


####################
# Static functions #
####################

def handle_brew(request):
    """
    Handles the specifics of a brew request

    Parameters:
        request (HTPCPRequest): the recieved request

    Returns:
        response (Response): the response appriotate for the request
    """
    
    if request.type == "coffee":
        pot = CoffeePot(request.pot_designator, request.additions)

    else:
        pot = TeaPot(request.pot_designator, request.additions, request.tea_type)
    
    BREWING_POTS.append(pot)

    response_headers = dict()
    response_headers["Content-Type"] = request.headers["Content-Type"]
    return Response(200, "OK", response_headers=response_headers)

def handle_get(request):
    """
    Gets information for a specific pot if it exists and the request matches
    
    Parameters:
        request (HTPCPRequest): the recieved request

    Returns:
        response (Response): the response appriotate for the request
    """
    pot = next((p for p in BREWING_POTS if str(p) == request.uri), None)

    if not pot:
        raise errors.BrewNotStarted
    
    if request.type != pot.pot_type:
        if pot.pot_type == "tea":
            raise errors.ImATeapotError
        else:
            raise errors.InvalidContentType

    # ensure the additions sent in the request are the same as the ones in the current pot
    if Counter(request.additions) != Counter(pot.additions):
        raise errors.UnsupportedAdditions
    
    response_headers = dict()
    response_headers["Content-Type"] = request.headers["Content-Type"]
    return Response(200, "OK", response_headers=response_headers)


def handle_request(request):
    """
    Handles a HTCPCP request and returns the proper response

    Parameters:
        request (Request): the HTCPCP request in Request format

    Returns:
        response (Response): a response appropriate for the request
    """

    try:
        req = HTCPCPRequest(request)

    except errors.RequestError as e:
        return Response(e.code, e.reason_phrase)

    except Exception as e:
        return Response(400, "Bad Request")

    if req.uri == "/":
        alternates = ', '.join("{{\"/{}\" {{type message/teapot}}}}".format(tea) for tea in VALID_TEA_TYPES)
        response_headers = dict()
        response_headers["Alternates"] = alternates
        return Response(300, "Multiple Choices", response_headers=response_headers)
    
    try:
        if req.method == "BREW":
            response = handle_brew(request)

        elif req.method == "GET":
            response = handle_get(request)
    
    except errors.RequestError as e:
        return Response(e.code, e.reason_phrase)
    
    return response
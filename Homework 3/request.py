import errors

CRLF = '\r\n'

class Request(object):
    """
    Class to hold a general Request

    Attributes:
        request_line (string): the request line containing the request method, uri and version
        headers (dict): a dictionary containing the header names and associated values
        body (string): the body of the request
        content_type (string): the value from the Content-Type header, if none then "text"
    """
    def __init__(self, request_line, headers, body):
        self.request_line = self.validate_request_line(request_line)
        self.headers = self.validate_headers(headers)
        self.body = body

        if "Content-Type" not in self.headers:
            self.content_type = "text"
        else:
            self.content_type = self.headers["Content-Type"]

    def validate_request_line(self, request_line):
        """
        Validates that the request line has a supported method, a correct uri and correct version

        Parameters:
            request_line (string): the request line of the request

        Returns:
            request_line (string): the validate request line
        """
        self.request_line = request_line
        
        try:
            method, uri, version = request_line.split()
        except ValueError:
            raise errors.InvalidURI

        self.method = method
        self.uri = self.validate_uri(uri)
        self.version = version

        return request_line

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
            uri, query_string = uri.split("?", 1)
            self.query_string = query_string
        else:
            self.query_string = None

        return uri

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
            
            header_dict[name] = value

        return header_dict

####################
# Static functions #
####################

def request_from_string(request_string):
    """
    Parses a request from a string into a Request object

    Parameters:
        request_string (string): the contents of the request

    Returns:
        request (Request): A parsed and validated HTCPCPRequest 
    """
    request_headers, request_body = request_string.split(CRLF + CRLF)
    request_headers = request_headers.split(CRLF)
    request_line = request_headers[0]
    headers = request_headers[1:]

    return Request(request_line, headers, request_body)
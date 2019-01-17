import errors

VALID_METHODS = ['GET', 'BREW', 'POST', 'WHEN', 'PROPFIND']
VALID_VERSION = "HTCPCP/1.0"

class CoffeeRequest(object):
    """
    Class to hold a HTCPCP request
    """

    def __init__(self, method=None, uri=None, version=None, headers=None, body=None):
        self.method = self.validate_method(method)
        self.uri = self.validate_uri(uri)
        self.version = self.validate_version(version)
        self.headers = self.validate_headers(headers)
    
    def validate_method(self, method):
        
        if method not in VALID_METHODS:
            raise errors.UnsupportedMethod

        return method

    def validate_uri(self, uri):
        try:
            scheme, uri = uri.split("://")
            host, uri = uri.split("/")
        except ValueError:
            raise errors.InvalidURI
        
        self.scheme = scheme
        self.host = host
        
        return uri

    def validate_version(self, version):
        if version != VALID_VERSION:
            raise errors.InvalidVersion

        return version

    def validate_headers(self, headers):

        return self
    
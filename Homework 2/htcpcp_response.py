class HTCPCPResponse(object):
    """
    Class to represent a response for the HTCPCP protocol

    Attributes:
        response_code (int): the HTTP response code
        reasone_phrase (string): the reason for the response (ex: Forbidden)
        response_headers (dict): a dictionary of header names and values to include in the response
        response_body (string): the response body
    """
    CRLF = "\r\n"
    VERSION = "HTCPCP-TEA/1.0"

    def __init__(self, response_code, reason_phrase, response_headers=dict(), response_body=""):
        self.response_code = response_code
        self.reason_phrase = reason_phrase
        self.response_headers = response_headers
        self.response_body = response_body

    def __str__(self):
        """The output if someone was to print an instance of this class"""
        # add status line
        response_string = "{} {} {}{}".format(self.VERSION, self.response_code, self.reason_phrase, self.CRLF)

        # add response headers if any
        for header, value in self.response_headers.items():
            response_string += "{}: {}{}".format(header, value, self.CRLF)
        
        # add body if one
        response_string += "{}{}".format(self.CRLF, self.response_body)

        return response_string
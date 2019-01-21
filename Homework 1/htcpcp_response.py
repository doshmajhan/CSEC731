class HTCPCPResponse(object):
    CRLF = "\r\n"
    VERSION = "HTCPCP-TEA/1.0"

    def __init__(self, response_code, reason_phrase, response_headers=[], response_body=""):
        self.response_code = response_code
        self.reason_phrase = reason_phrase
        self.response_headers = response_headers
        self.response_body = response_body

    def __str__(self):
        # add status line
        response_string = "{} {} {}{}".format(self.VERSION, self.response_code, self.reason_phrase, self.CRLF)

        # add response headers if any
        for header in self.response_headers:
            response_string += "{}{}".format(header, self.CRLF)
        
        # add body if one
        response_string += "{}{}".format(self.CRLF, self.response_body)

        return response_string
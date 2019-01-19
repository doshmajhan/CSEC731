class HTCPCPResponse(object):
    
    VERSION = "HTCPCP-TEA/1.0"

    def __init__(self, response_code, reason_phrase, response_headers=[], response_body=""):
        self.response_code = response_code
        self.reason_phrase = reason_phrase
        self.response_headers = response_headers
        self.response_body = response_body

    def __str__(self):
        # add status line
        response_string = "{} {} {}\r\n".format(self.VERSION, self.response_code, self.reason_phrase)

        # add response headers if any
        for header in self.response_headers:
            response_string += "{}\r\n".format(header)
        
        # add body if one
        response_string += "\r\n{}".format(self.response_body)

        return response_string
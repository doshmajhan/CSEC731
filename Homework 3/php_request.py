import os
import subprocess
import errors
from response import Response

CRLF = "\r\n"


class PhpRequest(object):
    """
    Wrapper to pass arguments to the `php-cgi` command line tool

    Attributes:
        PHP_CGI (string): the php-cgi executable to use
        method (string): the method used to submit the command
        parameters (string): the parameters to pass to the php script
        script_name (string): the name of the php script to execute
        environment (dict): a dictonary of key value pairs for the bash environment to execute in
    """

    PHP_CGI = "php-cgi"

    def __init__(self, request):
        """
        Parameters:
            request (Request): a request object containing the parsed PHP request
        """
        # trim leading /
        self.script_name = request.uri[1:]
        self.method = request.method

        self.environment = dict(os.environ)
        self.environment["REQUEST_METHOD"] = self.method
        self.environment["SCRIPT_FILENAME"] = self.script_name
        self.environment["SERVER_PROTOCOL"] = "HTTP/1.1"
        self.environment["REMOTE_HOST"] = "127.0.0.1"

        if self.method == "GET":
            self.parameters = request.query_string
            self.environment["QUERY_STRING"] = self.parameters
            self.environment["REDIRECT_STATUS"] = "0"
        elif self.method == "POST":
            self.parameters = request.body
            self.environment["REDIRECT_STATUS"] = "1"
            self.environment["GATEWAY_INTERFACE"] = "CGI/1.1"
            self.environment["CONTENT_LENGTH"] = str(len(self.parameters))
            self.environment["CONTENT_TYPE"] = "application/x-www-form-urlencoded"
        else:
            raise errors.UnsupportedMethod

    def execute(self):
        """
        Executes the php-cgi command with the premade environment
        and returns the output

        Returns:
            output (string): the output of the php-cgi command
        """
        process = subprocess.Popen(
            [self.PHP_CGI],
            env=self.environment,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE
        )

        out, err = process.communicate(str.encode(self.parameters))
        print("PHP stderr: {}".format(err))
        return out


####################
# Static functions #
####################

def handle_request(request):
    """
    Handles a PHP request and returns the proper response

    Parameters:
        request (Request): the PHP request in Request format

    Returns:
        response (Response): a 200 OK response with the php execution output as the body
    """
    php_req = PhpRequest(request)
    output = php_req.execute()
    headers, body = output.decode().split(CRLF + CRLF)

    response_headers = dict()
    response_headers["Content-Type"] = "text/plain"
    return Response(200, "OK", response_headers=response_headers, response_body=body)
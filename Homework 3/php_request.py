import os
import subprocess
import errors

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

    def __init__(self, method, script_name, parameters):
        """
        Parameters:
            method (string): method of the request
            script_name (string): name of the php file to execute
            parameters (string): a string of name value pairs
        """
        self.script_name = script_name
        self.parameters = parameters
        self.method = method

        self.environment = dict(os.environ)
        self.environment["REQUEST_METHOD"] = self.method
        self.environment["SCRIPT_FILENAME"] = self.script_name

        if self.method == "GET":
            self.environment["QUERY_STRING"] = self.parameters
            self.environment["REDIRECT_STATUS"] = "0"
        elif self.method == "POST":
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
            output(string): the output of the php-cgi command
        """
        process = subprocess.Popen(
            [self.PHP_CGI],
            env=self.environment,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE
        )

        out, err = process.communicate(str.encode(self.parameters))
        print(err)
        return out
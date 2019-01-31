import subprocess

class PHP(object):
    """
    Wrapper to pass arguments to the `php-cgi` command line tool

    Attributes:
        method (string): the method used to submit the command
        content (string): the php content to execute
    """
    def __init__(self, method, content):
        self.method = method
        self.content = content

    def execute(self):
        pass
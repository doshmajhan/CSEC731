#!/usr/bin/python

"""
    File to take in a parse a HTCPCP-TEA request and provide the appropriate source

    Author: Cameron Clark
    Created: 1/15/19
"""

import argparse
import sys
import errors
from coffee_request import CoffeeRequest

CRLF = "\r\n"
VALID_SERVER_TYPES = ["teapot", "coffee-pot"]


def parse_request(server_type, request_string):
    """
    Parses a HTCPCP-TEA request

    Parameters:
        server_type (string): the type of server, either teapot or coffee-pot
        request_string (string): the contents of the request

    Returns:
        response (string): A reponse string in the proper format 
    """
    response = ""
    request_headers, request_body = request_string.split("\n\n")
    request_headers = request_headers.split("\n")
    request_line = request_headers[0]
    headers = request_headers[1:]

    print(request_line)
    print(headers)
    print(request_body)

    parts = request_line.split()
    if len(parts) != 3:
        raise errors.InvalidRequestLine


    request = CoffeeRequest(
        method=parts[0], 
        uri=parts[1], 
        version=parts[2], 
        headers=headers, 
        body=request_body
    )

    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parses a HTCPCP-TEA request and provide the appropriate source', add_help=True)
    parser.add_argument('-t', dest='type', help='The type of server to emulate (teapot or coffee-pot)', required=True)
    parser.add_argument('-f', dest='file', help='The file containing the HTCPCP request', required=True)
    args = parser.parse_args()

    server_type = args.type
    file = args.file

    if server_type not in VALID_SERVER_TYPES:
        print("Non-valid server type used: {}".format(server_type))
        sys.exit()
    
    with open(file) as f:
        request = f.read()
    
    response = parse_request(server_type, request)
    print(response)

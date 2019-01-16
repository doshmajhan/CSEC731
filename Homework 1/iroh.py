#!/usr/bin/python

"""
    File to take in a parse a HTCPCP-TEA request and provide the appropriate source

    Author: Cameron Clark
    Created: 1/15/19
"""

import argparse
import sys

CRLF = "\r\n"
VALID_SERVER_TYPES = ["teapot", "coffee-pot"]


def parse_request_line(request_line):
    """
    Parses the request line of the recieved request to ensure if fits the format

    Parameters:
        request_line (string): the request line taken from the recieved request
    
    Returns:
    """
    pass

def parse_request(server_type, request):
    """
    Parses a HTCPCP-TEA request

    Parameters:
        server_type (string): the type of server, either teapot or coffee-pot
        request (string): the contents of the request

    Returns:
        response (string): A reponse string in the proper format 
    """
    response = ""
    print(request)
    request_line = request[0]
    headers = request[:-1]

    parse_request_line(request_line)
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
        request = [x.replace("\n", "") for x in f.readlines()]
    
    response = parse_request(server_type, request)
    print(response)


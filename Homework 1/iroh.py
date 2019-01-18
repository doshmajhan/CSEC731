#!/usr/bin/python

"""
    File to take in a parse a HTCPCP-TEA request and provide the appropriate source

    Author: Cameron Clark
    Created: 1/15/19
"""

import argparse
import errors
from htcpcp_request import HTCPCPRequest

CRLF = "\r\n"


def parse_request(request_string):
    """
    Parses a HTCPCP-TEA request

    Parameters:
        request_string (string): the contents of the request

    Returns:
        response (string): A reponse string in the proper format 
    """
    response = ""
    request_headers, request_body = request_string.split("\n\n")
    request_headers = request_headers.split("\n")
    request_line = request_headers[0]
    headers = request_headers[1:]

    parts = request_line.split()
    if len(parts) != 3:
        raise errors.InvalidRequestLine

    # TODO HANDLE / URI
    
    try:
        request = HTCPCPRequest(
            method=parts[0], 
            uri=parts[1], 
            version=parts[2], 
            headers=headers, 
            body=request_body
        )

    except errors.HTCPCPException as e:
        print(e.message)
        response = e.code

    else:
        response = 200

    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parses a HTCPCP-TEA request and provide the appropriate source', add_help=True)
    parser.add_argument('-f', dest='file', help='The file containing the HTCPCP request', required=True)
    args = parser.parse_args()

    file = args.file
    
    with open(file) as f:
        request = f.read()
    
    response = parse_request(request)
    print(response)

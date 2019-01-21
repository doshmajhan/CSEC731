#!/usr/bin/python

"""
    File to take in a parse a HTCPCP-TEA request and provide the appropriate response

    Author: Cameron Clark
    Created: 1/15/19
"""

import argparse
import errors
from htcpcp_request import HTCPCPRequest, VALID_TEA_TYPES
from htcpcp_response import HTCPCPResponse

CRLF = "\n"


def parse_request(request_string):
    """
    Parses a HTCPCP-TEA request

    Parameters:
        request_string (string): the contents of the request

    Returns:
        request (HTCPCP): A parsed and validated HTCPCPRequest 
    """
    request_headers, request_body = request_string.split(CRLF + CRLF)
    request_headers = request_headers.split(CRLF)
    request_line = request_headers[0]
    headers = request_headers[1:]

    return HTCPCPRequest(request_line, headers, request_body)


def handle_request(request_string):
    """
    Handles a HTCPCP request and returns the proper response

    Parameters:
        request_string (string): the HTCPCP request in string format

    Returns:
        response (HTCPCPResponse): a HTCPCP response object
    """

    try:
        request = parse_request(request_string)

    except errors.HTCPCPException as e:
        response = HTCPCPResponse(e.code, e.reason_phrase)
        return response

    except Exception as e:
        print(e.message)
        response = HTCPCPResponse(400, "Bad Request")
        return response

    if request.uri == "/":
        alternates = ', '.join("{{\"/{}\" {{type message/teapot}}}}".format(tea) for tea in VALID_TEA_TYPES)
        headers = ["Alternates: {}".format(alternates)]
        return HTCPCPResponse(300, "Multiple Choices", response_headers=headers)
    else:
        return HTCPCPResponse(200, "OK")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parses a HTCPCP-TEA request and provide the appropriate response', add_help=True)
    parser.add_argument('-f', dest='file', help='The file containing the HTCPCP-TEA request', required=True)
    args = parser.parse_args()

    file = args.file
    
    with open(file) as f:
        request = f.read()
    
    response = handle_request(request)
    print(response)

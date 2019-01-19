#!/usr/bin/python

"""
    File to take in a parse a HTCPCP-TEA request and provide the appropriate source

    Author: Cameron Clark
    Created: 1/15/19
"""

import argparse
import errors
from htcpcp_request import HTCPCPRequest
from htcpcp_response import HTCPCPResponse

CRLF = "\r\n"


def parse_request(request_string):
    """
    Parses a HTCPCP-TEA request

    Parameters:
        request_string (string): the contents of the request

    Returns:
        request (HTCPCP): A parsed and validated HTCPCPRequest 
    """
    request_headers, request_body = request_string.split("\n\n")
    request_headers = request_headers.split("\n")
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
        print(e.message)
        response = HTCPCPResponse(e.code, e.reason_phrase)
        return response

    except Exception as e:
        print(e.message)
        response = HTCPCPResponse(400, "Bad Request")
        return response

    if request.uri == "/":
        response_code = 300
        reason_phrase = "Multiple Choices"
    else:
        response_code = 200
        reason_phrase = "OK"

    response = HTCPCPResponse(response_code, reason_phrase)

    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parses a HTCPCP-TEA request and provide the appropriate source', add_help=True)
    parser.add_argument('-f', dest='file', help='The file containing the HTCPCP request', required=True)
    args = parser.parse_args()

    file = args.file
    
    with open(file) as f:
        request = f.read()
    
    response = handle_request(request)
    print(response)

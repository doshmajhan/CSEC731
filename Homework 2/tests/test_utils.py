import socket
import sys
sys.path.append("..")
from htcpcp_response import HTCPCPResponse

CRLF = "\r\n"
HOST = "127.0.0.1"
PORT = 9999


def send_request(request):
    """
    Sends a request to the local server

    Parameters:
        request (string): the mock request to send

    Returns:
        response (HTCPCPResponse): the returned response
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(request)
    data = s.recv(1000000)
    print(data)
    s.shutdown(1)
    s.close()
    return parse_response(data)


def parse_response(response):
    """
    Parses a string response into a HTCPCP response

    Parmeters:
        response (string): the response data recieved in string form
    
    Returns:
        response (HTCPCPResponse): the HTCPCPResponse object
    """
    response_headers, response_body = response.split(CRLF + CRLF)
    status_line, response_headers = response_headers.split(CRLF, 1)
    response_headers = response_headers.split(CRLF)
    print(response_headers)
    headers_dict = dict()

    for header in response_headers:
        print(header)
        name, value = header.split(":")
        # trim leading whitespace
        headers_dict[name] = value[1:]
    
    status_line = status_line.split()
    status_code = int(status_line[1])
    reason = status_line[2:]
    
    return HTCPCPResponse(status_code, reason, response_headers=headers_dict, response_body=response_body)
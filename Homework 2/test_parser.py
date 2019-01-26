from os import listdir
from os.path import isfile, join
import socket


EXAMPLE_REQUESTS_DIR = "example_requests/"
CRLF = "\r\n"
HOST = "127.0.0.1"
PORT = 9999


def test_parser():
    example_requests = [f for f in listdir(EXAMPLE_REQUESTS_DIR) if isfile(join(EXAMPLE_REQUESTS_DIR, f))]
    for request in example_requests:
        expected_code = int(request.replace("request", "").split("-")[0])
        
        with open(join(EXAMPLE_REQUESTS_DIR, request)) as f:
            request_string = f.read().replace("\n", "\r\n")
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(request_string)
        data = s.recv(1000000)
        print(data)
        s.shutdown(1)
        s.close()

        response_headers, response_body = data.split(CRLF)
        status_line = response_headers.split(CRLF, 1)
        response_headers = response_headers[1:].split(CRLF)

        version, status_code, reason = status_line.split()

        assert int(status_code) == expected_code
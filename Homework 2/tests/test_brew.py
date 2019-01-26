from os import listdir
from os.path import isfile, join
import socket
from test_utils import send_request

CRLF = "\r\n"

def start_brew():
    request = "BREW /pot-1 HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/coffee-pot-command{0}" \
        "Accept-Additions: Cream; Skim; Almond; Sugar{0}{0}".format(CRLF)

    response = send_request(request)
    assert response.response_code == 200

def testbrew():
    start_brew()
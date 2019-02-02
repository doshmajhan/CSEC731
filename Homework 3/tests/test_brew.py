from os import listdir
from os.path import isfile, join
import socket
from test_utils import send_request, CRLF


def brew_coffee():
    valid_request = "BREW /pot-1 HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/coffee-pot-command{0}" \
        "Accept-Additions: Cream; Skim; Almond; Sugar{0}{0}".format(CRLF)

    response = send_request(valid_request)
    assert response.response_code == 200
    assert response.response_headers["Content-Type"] == "message/coffee-pot-command"

    # second brew request for same pot should produce 403
    response = send_request(valid_request)
    assert response.response_code == 403

    # should fail because cheese is not a valid addition
    request_403 = "BREW /pot-2 HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/coffee-pot-command{0}" \
        "Accept-Additions: Cream; Cheese; Almond; Sugar{0}{0}".format(CRLF)

    response = send_request(request_403)
    assert response.response_code == 403

def brew_tea():
    valid_request = "BREW /pot-3/black HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/teapot{0}" \
        "Accept-Additions: Cream; Skim; Almond; Sugar{0}{0}".format(CRLF)

    response = send_request(valid_request)
    assert response.response_code == 200
    assert response.response_headers['Content-Type'] == "message/teapot"

    # second brew request for same pot should produce 403
    response = send_request(valid_request)
    assert response.response_code == 403

    # should fail because cheese is not a valid tea type
    request_403 = "BREW /pot-2/cheese HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/teapot{0}" \
        "Accept-Additions: Cream; Almond; Sugar{0}{0}".format(CRLF)

    response = send_request(request_403)
    assert response.response_code == 403


def get_coffee_pot():
    valid_request = "GET /pot-1?Cream&Skim&Almond&Sugar HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/coffee-pot-command{0}{0}".format(CRLF)

    response = send_request(valid_request)
    assert response.response_code == 200
    assert response.response_headers["Content-Type"] == "message/coffee-pot-command"


    # should fail, additions dont match original brew
    request_403 = "GET /pot-1?Cream&Skim&Almond HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/coffee-pot-command{0}{0}".format(CRLF)

    response = send_request(request_403)
    assert response.response_code == 403


    # should fail because brewing hasnt started for pot-2 yet
    request_404 = "GET /pot-2?Cream&Skim&Almond&Sugar HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/coffee-pot-command{0}{0}".format(CRLF)

    response = send_request(request_404)
    assert response.response_code == 404

    # should fail because we have the wrong content type
    request_400 = "GET /pot-1?Cream&Skim&Almond&Sugar HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/teapot{0}{0}".format(CRLF)

    response = send_request(request_400)
    assert response.response_code == 400


def get_tea_pot():
    valid_request = "GET /pot-3/black?Cream&Skim&Almond&Sugar HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/teapot{0}{0}".format(CRLF)

    response = send_request(valid_request)
    assert response.response_code == 200
    assert response.response_headers['Content-Type'] == "message/teapot"


    # should fail, additions dont match original brew
    request_403 = "GET /pot-3/black?Cream&Skim&Almond HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/teapot{0}{0}".format(CRLF)

    response = send_request(request_403)
    assert response.response_code == 403


    # should fail because brewing hasnt started for pot-2 yet
    request_404 = "GET /pot-2/green?Cream&Skim&Almond&Sugar HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/teapot{0}{0}".format(CRLF)

    response = send_request(request_404)
    assert response.response_code == 404

    # should fail because we have the wrong content type
    request_418 = "GET /pot-3/black?Cream&Skim&Almond&Sugar HTCPCP-TEA/1.0{0}" \
        "Content-Type: message/coffee-pot-command{0}{0}".format(CRLF)

    response = send_request(request_418)
    assert response.response_code == 418


def tes_server():
    brew_coffee()
    brew_tea()
    get_coffee_pot()
    get_tea_pot()
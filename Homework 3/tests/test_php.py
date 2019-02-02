import sys
from test_utils import send_request, CRLF
sys.path.append("..")
from php_request import PhpRequest


def test_get():
    valid_request = "GET /www/index.php?test=doshget HTCPCP-TEA/1.0{0}" \
        "Content-Type: application/x-www-form-urlencoded{0}{0}".format(CRLF)
    
    response = send_request(valid_request)
    print(response)
    assert response.response_code == 200

def test_post():
    valid_request = "POST /www/index.php HTCPCP-TEA/1.0{0}" \
        "Content-Type: application/x-www-form-urlencoded{0}{0}" \
        "test=doshpost".format(CRLF)
    
    response = send_request(valid_request)
    print(response)
    assert response.response_code == 200
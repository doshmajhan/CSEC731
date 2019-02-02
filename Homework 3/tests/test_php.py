import sys
sys.path.append("..")
from php_request import PhpRequest

TEST_FILE = "index.php"


def execute_php(method, parameters):
    php_page = PhpRequest(method, TEST_FILE, parameters)
    return php_page.execute()

def tes_get():
    parameters = "test=doshget"
    output = execute_php("GET", parameters)
    print(output)
    assert True

def tes_post():
    parameters = "test=doshpost"
    output = execute_php("POST", parameters)
    print(output)
    assert True
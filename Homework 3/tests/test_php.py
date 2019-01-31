import sys
sys.path.append("..")
from php_wrapper import Php

TEST_FILE = "index.php"


def execute_php(method, parameters):
    php_page = Php(method, TEST_FILE, parameters)
    return php_page.execute()

def test_get():
    parameters = "test=doshget"
    output = execute_php("GET", parameters)
    print(output)
    assert True

def test_post():
    parameters = "test=doshpost"
    output = execute_php("POST", parameters)
    print(output)
    assert True
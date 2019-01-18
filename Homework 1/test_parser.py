from os import listdir
from os.path import isfile, join
import iroh

EXAMPLE_REQUESTS_DIR = "example_requests/"

def test_parser():
    example_requests = [f for f in listdir(EXAMPLE_REQUESTS_DIR) if isfile(join(EXAMPLE_REQUESTS_DIR, f))]
    for request in example_requests:
        with open(join(EXAMPLE_REQUESTS_DIR, request)) as f:
            request_string = f.read()
        
        print(request)
        expected_code = int(request.replace("request", "").split("-")[0])
        assert expected_code == iroh.parse_request(request_string)

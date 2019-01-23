import socket
import sys
import threading
import errors
from htcpcp_request import HTCPCPRequest, VALID_TEA_TYPES
from htcpcp_response import HTCPCPResponse

CRLF = "\r\n"


class HTCPCPServer(object):
    """
    Handles requests recieved and perform the proper actions
    returning any response info if required

    Attributes:
        address (string): the ip address to listen on
        port (int): the port to bind to
    """

    def __init__(self, address, port):
        self.address = address
        self.port = port

    

    def start(self):
        print("Starting listener on {}:{}".format(self.address, self.port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.address, self.port))
        self.sock.listen(2)

        while True:
            #Accept request and start a new thread
            conn, addr = self.sock.accept()
            request = conn.recv(8192)

            print("Request recieved from {}".format(addr))
            request_handler = threading.Thread(target=self.handle_request, args=(request, conn))
            request_handler.daemon=True

            try:
                request_handler.start()

            except (KeyboardInterrupt, SystemExit):
                self.sock.close()
                sys.exit()


    def parse_request(self, request_string):
        """
        Parses a HTCPCP-TEA request

        Parameters:
            request_string (string): the contents of the request
            addr (tuple): a tuple containing the address and port the request came from

        Returns:
            request (HTCPCP): A parsed and validated HTCPCPRequest 
        """
        request_headers, request_body = request_string.split(CRLF + CRLF)
        request_headers = request_headers.split(CRLF)
        request_line = request_headers[0]
        headers = request_headers[1:]

        return HTCPCPRequest(request_line, headers, request_body)


    def handle_request(self, request_string, conn):
        """
        Handles a HTCPCP request and returns the proper response

        Parameters:
            request_string (string): the HTCPCP request in string format
            conn (socket): A socket object used to send data back to the client
        """

        try:
            request = self.parse_request(request_string)

        except errors.HTCPCPException as e:
            response = HTCPCPResponse(e.code, e.reason_phrase)
            conn.sendall(str(response))
            return

        except Exception as e:
            print(e.message)
            response = HTCPCPResponse(400, "Bad Request")
            conn.sendall(str(response))
            return

        if request.uri == "/":
            alternates = ', '.join("{{\"/{}\" {{type message/teapot}}}}".format(tea) for tea in VALID_TEA_TYPES)
            headers = ["Alternates: {}".format(alternates)]
            response = HTCPCPResponse(300, "Multiple Choices", response_headers=headers)
        else:
            response = HTCPCPResponse(200, "OK")
        

        conn.sendall(str(response))

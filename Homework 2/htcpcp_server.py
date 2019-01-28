import logging
import socket
import sys
import threading
from collections import Counter
import errors
from htcpcp_request import HTCPCPRequest, VALID_TEA_TYPES
from htcpcp_response import HTCPCPResponse
from coffee_pot import CoffeePot
from tea_pot import TeaPot


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
        self.brewing_pots = list()

    def start(self):
        print("Starting listener on {}:{}".format(self.address, self.port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.address, self.port))
        self.sock.listen(2)

        while True:
            #Accept request and start a new thread
            conn, addr = self.sock.accept()
            request = conn.recv(8192)
            request = request.decode()

            print("Request recieved from {}".format(addr))
            request_handler = threading.Thread(target=self.connection_handler, args=(request, conn))
            request_handler.daemon = True

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
            request (HTCPCPRequest): A parsed and validated HTCPCPRequest 
        """
        request_headers, request_body = request_string.split(CRLF + CRLF)
        request_headers = request_headers.split(CRLF)
        request_line = request_headers[0]
        headers = request_headers[1:]

        return HTCPCPRequest(request_line, headers, request_body)

    def handle_brew(self, request):
        """
        Handles the specifics of a brew request

        Parameters:
            request (HTPCPRequest): the recieved request

        Returns:
            response (HTCPCPResponse): the response appriotate for the request
        """
        
        if request.type == "coffee":
            pot = CoffeePot(request.pot_designator, request.additions)

        else:
            pot = TeaPot(request.pot_designator, request.additions, request.tea_type)
        
        self.brewing_pots.append(pot)

        response_headers = dict()
        response_headers["Content-Type"] = request.headers["Content-Type"]
        return HTCPCPResponse(200, "OK", response_headers=response_headers)


    def handle_get(self, request):
        """
        Gets information for a specific pot if it exists and the request matches
        
        Parameters:
            request (HTPCPRequest): the recieved request

        Returns:
            response (HTCPCPResponse): the response appriotate for the request
        """
        pot = next((p for p in self.brewing_pots if str(p) == request.uri), None)

        if not pot:
            raise errors.BrewNotStarted
        
        if request.type != pot.pot_type:
            if pot.pot_type == "tea":
                raise errors.ImATeapotError
            else:
                raise errors.InvalidContentType

        if Counter(request.additions) != Counter(pot.additions):
            raise errors.UnsupportedAdditions
        
        response_headers = dict()
        response_headers["Content-Type"] = request.headers["Content-Type"]
        return HTCPCPResponse(200, "OK", response_headers=response_headers)

    def handle_request(self, request_string):
        """
        Handles a HTCPCP request and returns the proper response

        Parameters:
            request_string (string): the HTCPCP request in string format

        Returns:
            response (HTCPCPResponse): a response appropriate for the request
        """

        try:
            request = self.parse_request(request_string)

        except errors.HTCPCPException as e:
            print(e.message)
            return HTCPCPResponse(e.code, e.reason_phrase)

        except Exception as e:
            print(e)
            return HTCPCPResponse(400, "Bad Request")

        if request.uri == "/":
            alternates = ', '.join("{{\"/{}\" {{type message/teapot}}}}".format(tea) for tea in VALID_TEA_TYPES)
            response_headers = dict()
            response_headers["Alternates"] = alternates
            return HTCPCPResponse(300, "Multiple Choices", response_headers=response_headers)
        
        try:
            if request.method == "BREW":
                response = self.handle_brew(request)

            elif request.method == "GET":
                response = self.handle_get(request)
        
        except errors.HTCPCPException as e:
            print(e.message)
            return HTCPCPResponse(e.code, e.reason_phrase)
        
        # request complete successfully, log and return
        logging.info(request.request_line)
        return response

    def connection_handler(self, request_string, conn):
        """
        Handles a new connection, and responds if necessary

        Parameters:
            request_string (string): the HTCPCP request in string format
            conn (socket): A socket object used to send data back to the client
        """
        response = self.handle_request(request_string)
        conn.sendall(str(response).encode())

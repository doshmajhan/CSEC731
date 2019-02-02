import logging
import socket
import sys
import threading
import errors
import request
import htcpcp_request
import php_request
from response import Response
import traceback

CRLF = "\r\n"


class HTTPServer(object):
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

    def handle_request(self, request_string):
        """
        Handles a Request and returns the proper response

        Parameters:
            request_string (string): the request in string format

        Returns:
            response (Response): a response appropriate for the request
        """

        try:
            req = request.request_from_string(request_string)

        except errors.RequestError as e:
            traceback.print_exc()
            return Response(e.code, e.reason_phrase)

        except Exception as e:
            traceback.print_exc()
            return Response(500, "Internal Server Error")

        try:

            if req.content_type == "message/coffee-pot-command" or req.content_type == "message/teapot":
                response = htcpcp_request.handle_request(req)
            elif req.content_type == "application/x-www-form-urlencoded":
                response = php_request.handle_request(req)
            else:
                raise errors.InvalidContentType
        
        except errors.RequestError as e:
            traceback.print_exc()
            return Response(e.code, e.reason_phrase)

        except Exception as e:
            traceback.print_exc()
            return Response(500, "Internal Server Error")
        
        # request complete successfully, log and return
        logging.info(req.request_line)
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

#!/usr/bin/python

"""
    File to take in a parse a HTCPCP-TEA request and provide the appropriate response

    Author: Cameron Clark
    Created: 1/15/19
"""

import argparse
import logging
from htcpcp_server import HTCPCPServer

LOG_FILE = "server.log"
logging.basicConfig(filenanme=LOG_FILE,level=logging.DEBUG)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Starts a HTCPCP-TEA server on the given address and port', add_help=True)
    parser.add_argument('-p', dest='port', help='The port for the server to bind to', type=int, required=True)
    parser.add_argument('-l', dest='address', help='The address to listen on', required=True)
    args = parser.parse_args()

    server = HTCPCPServer(args.address, args.port)
    server.start()

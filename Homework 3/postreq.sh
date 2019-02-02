#!/bin/bash

export GATEWAY_INTERFACE="CGI/1.1"
export SCRIPT_FILENAME="/home/nerdprof/postdemo.php"
export REQUEST_METHOD="POST"
export SERVER_PROTOCOL="HTTP/1.1"
export REMOTE_HOST="127.0.0.1"
export CONTENT_LENGTH=29
export BODY="example1=Hello&example2=World"
export CONTENT_TYPE="application/x-www-form-urlencoded"

exec echo "$BODY" | php-cgi
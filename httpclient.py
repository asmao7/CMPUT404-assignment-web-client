#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# Copyright @student submitting: Asma Omar
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
#import urllib.parse
from urllib.parse import urlparse, urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    # get code if it starts with http
    def get_code(self, data):
        code = data.split()[1]
        return int(code)
        

    def get_headers(self,data):
        return None

    # return body from data
    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def parse(self, url):
        parse_result = urlparse(url)
        print("PARSE RESULTS: ", parse_result)
        self.host_name = parse_result.hostname #parse_result.netloc
        print("HOST NAME IS: ", self.host_name)
        self.host = self.host_name.split(":")[0]
        print("HOST IS: ", self.host)
        self.port = parse_result.port
        print("PORT IS: ", self.port)
        if(self.port == None):
            self.port = 80
        self.path = parse_result.path
        if(self.path == ""):
            self.path = "/"


    def GET(self, url, args=None):
        # if not http in url 404 error otherwise connect
        if('http' not in url and 'http'.upper() not in url and 'https' not in url and 'https'.upper() not in url):
            code = 404
            body = 'HTTP/1.1 404 Not Found'
            return HTTPResponse(code, body)
        
        # parse url
        self.parse(url)
        request = f"GET {(self.path)} HTTP/1.1\r\nHost: {(self.host_name)} \r\nConnection: close\r\n\r\n"
        print("REQUEST IS: ", request)

        # connect
        self.connect(self.host, self.port)
        self.sendall(request)
        
        # receive data
        data = self.recvall(self.socket)
        self.close()

        # get code and body then return HTTP response
        code = self.get_code(data)
        body = self.get_body(data)
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # if not an http return 404 Npt FOund?
        if('http' not in url and 'http'.upper() not in url and 'https' not in url and 'https'.upper() not in url):
            code = 404
            body = 'HTTP/1.1 404 Not Found'
            return HTTPResponse(code, body)
           
        # parse url
        self.parse(url)
        if(args != None):
            body = urlencode(args)
            length = f"\nContent-Length: {str(len(body))}"
        else:
            length = f"\nContent-Length: {str(0)}"
            body = ""
        
        #length = f"\nCOntent-Length: {len(body)}"
        print("Length is: ", length)
        request = f"POST {(self.path)} HTTP/1.1\r\nHost: {(self.host_name)}Connection: close\r\nContent-Type: application/x-www-form-urlencoded\r{(length)}\r\n\r\n{(body)}"
        print("POST REQUEST IS: ", request)

        # connect 
        self.connect(self.host, self.port)
        self.sendall(request)
        data = self.recvall(self.socket)
        self.close()

        # get code and body then return response
        code = self.get_code(data)
        body = self.get_body(data)
        
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))



# TO CITE:
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
# https://docs.plone.org/develop/plone/serving/http_request_and_response.html
# https://docs.python.org/3/library/urllib.parse.html
#
#
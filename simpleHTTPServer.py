#!/usr/bin/env python
from urlparse import parse_qsl
from urlparse import parse_qs
import BaseHTTPServer

server_class = BaseHTTPServer.HTTPServer

class handler_class( \
      BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = parse_qs(self.headers['content-type'],keep_blank_values=1)
        if ctype == 'multipart/form-data':
            postvars = parse_qs(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length), 
                    keep_blank_values=1)
        else:
            postvars = {}
        print(postvars)
        return postvars

def run(server_class, handler_class):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()



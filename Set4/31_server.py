#!/usr/bin/env python3
"""."""
import http.server
from hmac import hmac
from urllib.parse import parse_qs, urlparse
from time import sleep
from itertools import zip_longest

KEY = b'you never know!'
PORT = 8080

def insecure_compare(s1, s2):
    for (c1, c2) in zip_longest(s1, s2):
        if c1 == c2:
            sleep(0.01)
        else:
            return False
    return True

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        qs = urlparse(self.path).query
        p = parse_qs(qs)
        if 'file' in p and 'signature' in p:
            fname, sig = p['file'][0].encode(), p['signature'][0].encode()
            #print('FNAME:', fname)
            #print('SIG:', sig)
            if insecure_compare(hmac(KEY, fname), sig):
                return self.valid('Access to ' + p['file'][0] + ' granted!')
            else:
                return self.invalid()
        return self.valid('What are you looking for?')

    def valid(self, msg):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(msg.encode())
        return
    
    def invalid(self):
        self.send_error(401, 'Bad HMAC!')
        return


try:
    server = http.server.HTTPServer(('127.0.0.1', PORT), Handler)
    print('Started HTTP server on port', PORT)
    server.serve_forever()
except KeyboardInterrupt:
    print('Server interrupted, stopping')
    server.socket.close()

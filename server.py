#!/usr/bin/env python
from app import make_app
import random
import socket
from StringIO import StringIO
from sys import stderr
import time
from urlparse import urlparse
from wsgiref.validate import validator

def handle_connection(conn, port):
    request = conn.recv(1)
    
    if not request:
        print 'Error, remote client closed connection without sending anything'
        return

    count = 0
    env = {}
    while request[-4:] != '\r\n\r\n':
        request += conn.recv(1)

    request, data = request.split('\r\n',1)
    headers = {}
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        headers[k.lower()] = v

    path = urlparse(request.split(' ', 3)[1])
    env['REQUEST_METHOD'] = 'GET'
    env['PATH_INFO'] = path[2]
    env['QUERY_STRING'] = path[4]
    env['CONTENT_TYPE'] = 'text/html'
    env['CONTENT_LENGTH'] = str(0)
    env['SCRIPT_NAME'] = ''
    env['SERVER_NAME'] = socket.getfqdn()
    env['SERVER_PORT'] = str(port)
    env['wsgi.version'] = (1, 0)
    env['wsgi.errors'] = stderr
    env['wsgi.multithread']  = False
    env['wsgi.multiprocess'] = False
    env['wsgi.run_once']     = False
    env['wsgi.url_scheme'] = 'http'

    body = ''
    if request.startswith('POST '):
        env['REQUEST_METHOD'] = 'POST'
        env['CONTENT_LENGTH'] = headers['content-length']
        env['CONTENT_TYPE'] = headers['content-type']
        while len(body) < int(headers['content-length']):
            body += conn.recv(1)

    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

    env['wsgi.input'] = StringIO(body)
    my_app = make_app()
    validator_app = validator(my_app)
    result = my_app(env, start_response)
    for data in result:
        conn.send(data)
    conn.close()

def main(socketmodule=None):
    if socketmodule is None:
        socketmodule = socket

    s = socketmodule.socket()         # Create a socket object
    host = socketmodule.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))              # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                       # Now wait for client connection

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c, client_port)

if __name__ == '__main__':
    main()





###!/usr/bin/env python
##import random
##import socket
##import time
##from urlparse import urlparse
##from StringIO import StringIO
##from app import make_app
##from wsgiref.validate import validator
##from sys import stderr
##
##def handle_connection(conn, port):
##    """Takes a socket connection, and serves a WSGI app over it.
##        Connection is closed when app is served."""
##    
##    # Start reading in data from the connection
##    req = conn.recv(1)
##    count = 0
##    env = {}
##    while req[-4:] != '\r\n\r\n':
##        new = conn.recv(1)
##        if new == '':
##            return
##        else:
##            req += new
##
##    # Parse the headers we've received
##    req, data = req.split('\r\n',1)
##    headers = {}
##    for line in data.split('\r\n')[:-2]:
##        key, val = line.split(': ', 1)
##        headers[key.lower()] = val
##
##    # Parse the path and related env info
##    urlInfo = urlparse(req.split(' ', 3)[1])
##    env['REQUEST_METHOD'] = 'GET'
##    env['PATH_INFO'] = urlInfo[2]
##    env['QUERY_STRING'] = urlInfo[4]
##    env['CONTENT_TYPE'] = 'text/html'
##    env['CONTENT_LENGTH'] = str(0)
##    env['SCRIPT_NAME'] = ''
##    env['SERVER_NAME'] = socket.getfqdn()
##    env['SERVER_PORT'] = str(port)
##    env['wsgi.version'] = (1, 0)
##    env['wsgi.errors'] = stderr
##    env['wsgi.multithread']  = False
##    env['wsgi.multiprocess'] = False
##    env['wsgi.run_once']     = False
##    env['wsgi.url_scheme'] = 'http'
##
##    # Start response function for WSGI interface
##    def start_response(status, response_headers):
##        """Send the initial HTTP header, with status code 
##            and any other provided headers"""
##        
##        # Send HTTP status
##        conn.send('HTTP/1.0 ')
##        conn.send(status)
##        conn.send('\r\n')
##
##        # Send the response headers
##        for pair in response_headers:
##            key, header = pair
##            conn.send(key + ': ' + header + '\r\n')
##        conn.send('\r\n')
##    
##    # If we received a POST request, collect the rest of the data
##    content = ''
##    if req.startswith('POST '):
##        # Set up extra env variables
##        env['REQUEST_METHOD'] = 'POST'
##        env['CONTENT_LENGTH'] = str(headers['content-length'])
##        env['CONTENT_TYPE'] = headers['content-type']
##        # Continue receiving content up to content-length
##        cLen = int(headers['content-length'])
##        while len(content) < cLen:
##            content += conn.recv(1)
##        
##    # Set up a StringIO to mimic stdin for the FieldStorage in the app
##    env['wsgi.input'] = StringIO(content)
##    
##    # Get the application
##    wsgi_app = make_app()
##    
##    ## VALIDATION ##
##    wsgi_app = validator(wsgi_app)
##    ## VALIDATION ##
##
##    result = wsgi_app(env, start_response)
##
##    # Serve the processed data
##    for data in result:
##        conn.send(data)
##
##    # Close the connection; we're done here
##    conn.close()
##
##def main():
##    """Waits for a connection, then serves a WSGI app using handle_connection"""
##    # Create a socket object
##    sock = socket.socket()
##    
##    # Get local machine name (fully qualified domain name)
##    host = socket.getfqdn()
##
##    # Bind to a (random) port
##    port = random.randint(8000, 9999)
##    sock.bind((host, port))
##
##    print 'Starting server on', host, port
##    print 'The Web server URL for this would be http://%s:%d/' % (host, port)
##
##    # Now wait for client connection.
##    sock.listen(5)
##
##    print 'Entering infinite loop; hit CTRL-C to exit'
##    while True:
##        # Establish connection with client.    
##        conn, (client_host, client_port) = sock.accept()
##        print 'Got connection from', client_host, client_port
##        handle_connection(conn, client_port)
##        
### boilerplate
##if __name__ == "__main__":
##    main()

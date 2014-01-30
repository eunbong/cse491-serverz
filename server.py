#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
import urllib

# Global Variables

header = 'HTTP/1.0 200 OK\r\n' + \
         'Content-type: text/html\r\n' + \
         '\r\n'

header2 = 'HTTP/1.0 200 OK\r\n' + \
          'Content-type: application/x-www-form-urlencoded\r\n' + \
          '\r\n'

def handle_connection_default(conn, params):
    defaultRequest = header + '<h1>Hello, world.</h1>' + \
                     'This is yangeunb\'s Web server.'+ \
                     '<h1>home</h1>' + \
                     '<ul>' + \
                     '<li><a href="/content">Content</a></li>' + \
                     '<li><a href="/file">File</a></li>' + \
                     '<li><a href="/image">Image</a></li>' + \
                     '<li><a href="/form">Form</a></li>' +\
                     '</ul>'

    return defaultRequest
    
def connection_content(conn, params):
    request = header + '<h1>Here are some Contents</h1>'
    return request
    

def connection_file(conn, params):
    request = header + '<h1>Here is a File</h1>'
    return request

def connection_image(conn, params):
    request = header + '<h1>Here is an Image</h1>'
    return request

def connection_form(conn, params):
    request = header + \
              '<h1>Form</h1>' + \
              "<form action='/submit' method='GET'>"+\
              "First Name: <input type='text' name='firstname'><br></br>"+\
              "Last Name: <input type='text' name='lastname'><br></br>"+\
              "<input type='submit' name='submit'><br></br>"+\
              "</form>\r\n"

    return request

def connection_submit(conn, params):
    firstName = params['firstname'][0]
    lastName = params['lastname'][0]

    request = header + \
              '<h1>Hello %s %s</h1>'%(firstName,lastName)+\
              '<a href="/">Home</a><br></br>'+\
              "This is Eunbong's Web server."

    return request
        

def handle_connection_failure(conn, params):
    request = header + \
              '<h1>Bad Request</h1>'
    return request

def handle_post_connection(conn, params):
    request = header2 + '<h1>this is a post method</h1>' + \
              'This is yangeunb\'s Web server.'+ \
              '<h1>home</h1>' + \
              '<ul>' + \
              '<li><a href="/content">Content</a></li>' + \
              '<li><a href="/file">File</a></li>' + \
              '<li><a href="/image">Image</a></li>' + \
              '<li><a href="/form">Form</a></li>' +\
              '</ul>'
    return request
    
def handle_post_form(conn, params):
    request = header2 + \
              '<h1>Form</h1>' + \
              "<form action='/submit' method='POST'>"+\
              "First Name: <input type='text' name='firstname'><br></br>"+\
              "Last Name: <input type='text' name='lastname'><br></br>"+\
              "<input type='submit' name='submit'><br></br>"+\
              "</form>\r\n"
    return request

def handle_post_submit(conn, params):
    ''' this code is helping from Jason's code'''
    headers = []
    body_exist = False
    body = ""
    for line in params.split("\r\n"):
        if body_exist:
            body = line
            continue
        if line == "":
            body_exist = True
        headers.append(line)
    
    path = params.split()[1]
    para = parse_qs(body)

    firstName = para['firstname'][0]
    lastName = para['lastname'][0]

    request = header2 + \
              '<h1>this is a post method</h1><br></br>'+\
              '<h1>Hello %s %s</h1>'%(firstName,lastName)+\
              '<a href="/">Home</a><br></br>'+\
              "This is Eunbong's Web server."

    return request


def handle_connection(conn):
    requestInfo = conn.recv(1000)
    
    method = requestInfo.split()[0]

    response = ''
    
    if method == "GET":
        path = requestInfo.split()[1]
        params = parse_qs(urlparse(path)[4])
        real_path = urlparse(path)[2]
        if real_path == '/':
            response = handle_connection_default(conn, params)
        elif real_path == '/content':
            response = connection_content(conn, params)
        elif real_path == '/file':
            response = connection_file(conn, params)
        elif real_path == '/image':
            response = connection_image(conn, params)
        elif real_path == '/form':
            response = connection_form(conn, params)
        elif real_path == '/submit':
            response = connection_submit(conn, params)
        else:
            response = handle_connection_failure(conn, params)

    elif method == "POST":
        path = requestInfo.split()[1]
        
        if path == '/':
            response = handle_post_connection(conn, '')
        elif path == '/form':
            response = handle_post_form(conn, '')
        elif path == '/submit':
            response = handle_post_submit(conn, requestInfo)

    else:
            print 'Error: Invalid Request Made'

    conn.send(response)
    conn.close()


def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)
            
if __name__ == '__main__':
    main()


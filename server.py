#!/usr/bin/env python
import random
import socket
import time

beginner = 'HTTP/1.0 200 OK\r\n' + \
           'Content-type: text/html\r\n' + \
           '\r\n'
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
		requestInfo = c.recv(1000)
		requestType = requestInfo.split()[0]
		if requestType == "GET":
			requestURL = requestInfo.split()[1]

			if requestURL == '/':
				handle_connection(c)
			elif requestURL == '/content':
				connection_content(c)
			elif requestURL == '/file':
				connection_file(c)
			elif requestURL == '/image':
				connection_image(c)
			else:
				handle_connection_failure(c)

		elif requestType == "POST":
			handle_post_connection(c)

		else:
			print 'Error: Invalid Request Made'
			break


def handle_connection(conn):
	defaultRequest = beginner + '<h1>Hello, world.</h1>' + \
                                    'This is yangeunb\'s Web server.'+ \
                                    '<h1>/home</h1>' + \
			            '<ul>' + \
                                    '<li><a href="/content">Content</a></li>' + \
                                    '<li><a href="/file">File</a></li>' + \
			            '<li><a href="/image">Image</a></li>' + \
			            '</ul>'
	conn.send(defaultRequest)
	conn.close()

def connection_content(conn):
	request = beginner + '<h1>Here are some Contents</h1>'
        #conn.send(beginner)
        #conn.send('<h1>Here are some Contents</h1>')
	conn.send(request)
	conn.close()

def connection_file(conn):
        request = beginner + '<h1>Here is a File</h1>'
        conn.send(request)
        conn.close()

def connection_image(conn):
	request = beginner + '<h1>Here is an Image</h1>'
	conn.send(request)
	conn.close()

def handle_connection_failure(conn):
	request = beginner + '<h1>Bad Request</h1>'
	conn.send(request)
	conn.close()

def handle_post_connection(conn):
	request = beginner + '<h1>this is a post method</h1>'
	conn.send(request)
	conn.close()

if __name__ == '__main__':
	main()

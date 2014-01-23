import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    
    expected_return ='HTTP/1.0 200 OK\r\n' + \
                     'Content-type: text/html\r\n' + \
                     '\r\n' + \
                     '<h1>Hello, world.</h1>' + \
                     'This is yangeunb\'s Web server.'+ \
                     '<h1>/home</h1>' + \
                     '<ul>' + \
                     '<li><a href="/content">Content</a></li>' + \
                     '<li><a href="/file">File</a></li>' + \
                     '<li><a href="/image">Image</a></li>' + \
                     '</ul>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_connection_content():
    conn = FakeConnection("GET /Content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Here are some Contents</h1>'

    server.connection_content(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_connection_file():
    conn = FakeConnection("GET /File HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Here is a File</h1>'

    server.connection_file(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_connection_image():
    conn = FakeConnection("GET /Image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Here is an Image</h1>'
	
    server.connection_image(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_post_connection():
    conn = conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>this is a post method</h1>'

    server.handle_post_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_connection_failure():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Bad Request</h1>'
    
    server.handle_connection_failure(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

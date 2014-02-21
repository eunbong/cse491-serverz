<<<<<<< HEAD
import server

post_content_type = "Content-Type: application/x-www-form-urlencoded\r\n\r\n"

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

def test_handle_connection_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    msg = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn)

    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)
    
def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    msg = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn)

    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    msg = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn)

    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    msg = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn)

    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)

def test_get_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    msg = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn)

    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)

def test_404():
    conn = FakeConnection("GET /404 HTTP/1.0\r\n\r\n")
    msg = 'HTTP/1.0 404 Not Found\r\n'

    server.handle_connection(conn)

    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)

def test_submit_get():
    firstname = "Eunbong"
    lastname = "Yang"
    
    conn = FakeConnection("GET /submit?firstname={0}&lastname={1} \
                          HTTP/1.0\r\n\r\n".format(firstname, lastname))
    msg = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn)

    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)

def test_submit_post_urlencoded():
    firstname = "Eunbong"
    lastname = "Yang"
    name_info = "firstname={0}&lastname={1}\r\n".format(firstname, lastname)
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "Content-Length: 29\r\n" + \
                          post_content_type + \
                          name_info)
    msg = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn)

    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)

def test_submit_post_multipart():
    fake_info = "POST /submit HTTP/1.0\r\n" + \
                "Content-Length: 374\r\n" + \
                "Content-Type: multipart/form-data; " + \
                "boundary=32452685f36942178a5f36fd94e34b63\r\n\r\n" + \
                "--32452685f36942178a5f36fd94e34b63\r\n" + \
                "Content-Disposition: form-data; name=\"lastname\";" + \
                " filename=\"lastname\"\r\n\r\n" + \
                "Yang\r\n" + \
                "--32452685f36942178a5f36fd94e34b63\r\n" + \
                "Content-Disposition: form-data; name=\"firstname\";" + \
                " filename=\"firstname\"\r\n\r\n" + \
                "Eunbong\r\n" + \
                "--32452685f36942178a5f36fd94e34b63\r\n" + \
                "Content-Disposition: form-data; name=\"key\";" + \
                " filename=\"key\"\r\n\r\n" + \
                "value\r\n" + \
                "--32452685f36942178a5f36fd94e34b63--\r\n"
    
    conn = FakeConnection(fake_info)
    
    firstname = 'Eunbong'
    lastname = 'Yang'
    msg = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn)

    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)

def test_submit_post_404():
    conn = FakeConnection("POST /asdf HTTP/1.0\r\n" + \
                          "Content-Length: 0\r\n" + \
                          post_content_type
                         )
    server.handle_connection(conn)

    msg = 'HTTP/1.0 404 Not Found\r\n'

    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)
=======
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

def test_handle_connection_default():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    
    expected_return ='HTTP/1.0 200 OK\r\n' + \
                     'Content-type: text/html\r\n' + \
                     '\r\n' + \
                     '<h1>Hello, world.</h1>' + \
                     'This is yangeunb\'s Web server.'+ \
                     '<h1>home</h1>' + \
                     '<ul>' + \
                     '<li><a href="/content">Content</a></li>' + \
                     '<li><a href="/file">File</a></li>' + \
                     '<li><a href="/image">Image</a></li>' + \
                     '<li><a href="/form">Form</a></li>' +\
                     '</ul>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Here are some Contents</h1>'

    server.handle_connection(conn)
    
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Here is a File</h1>'

    server.handle_connection(conn)
    
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Here is an Image</h1>'

    server.handle_connection(conn)
    
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_connection_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Form</h1>' + \
                      "<form action='/submit' method='GET'>"+\
                      "First Name: <input type='text' name='firstname'><br></br>"+\
                      "Last Name: <input type='text' name='lastname'><br></br>"+\
                      "<input type='submit' name='submit'><br></br>"+\
                      "</form>\r\n"
    
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_connection_submit():
    conn = FakeConnection("GET /submit?firstname=Eunbong&lastname=Yang HTTP/1.0" + \
                          "HTTP/1.1\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello Eunbong Yang</h1>'+\
                      '<a href="/">Home</a><br></br>'+\
                      "This is Eunbong's Web server."

    server.handle_connection(conn)
    
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    
def test_handle_post_connection():
    conn = conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: application/x-www-form-urlencoded\r\n' + \
                      '\r\n' + \
                      '<h1>this is a post method</h1>' + \
                      'This is yangeunb\'s Web server.'+ \
                      '<h1>home</h1>' + \
                      '<ul>' + \
                      '<li><a href="/content">Content</a></li>' + \
                      '<li><a href="/file">File</a></li>' + \
                      '<li><a href="/image">Image</a></li>' + \
                      '<li><a href="/form">Form</a></li>' +\
                      '</ul>'

    server.handle_connection(conn)
    
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post_form():
    conn = FakeConnection("POST /form HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: application/x-www-form-urlencoded\r\n' + \
                      '\r\n' + \
                      '<h1>Form</h1>' + \
                      "<form action='/submit' method='POST'>"+\
                      "First Name: <input type='text' name='firstname'><br></br>"+\
                      "Last Name: <input type='text' name='lastname'><br></br>"+\
                      "<input type='submit' name='submit'><br></br>"+\
                      "</form>\r\n"
    
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    
def test_handle_post_submit():
    conn = FakeConnection("POST /submit HTTP/1.0\r\nHost: msu.edu\r\n\r\nfirstname=Eunbong&lastname=Yang")
    head = 'HTTP/1.0 200 OK\r\n' + \
           'Content-type: application/x-www-form-urlencoded\r\n' + \
           '\r\n'
    expected_return = head + \
                      '<h1>this is a post method</h1><br></br>'+\
                      '<h1>Hello Eunbong Yang</h1>'+\
                      '<a href="/">Home</a><br></br>'+\
                      "This is Eunbong's Web server."

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


>>>>>>> master

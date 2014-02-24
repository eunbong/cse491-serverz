#! /usr/bin/env python
import server

def test_error():
    conn = FakeConnection("GET /404NotFound HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if 'HTTP/1.0 404 Not Found' not in result:
        assert False
    else:
        pass

def test_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Hello, world!') not in result:
        assert False
    else:
        pass

def test_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Content Page') not in result:
        assert False
    else:
        pass

def test_File():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'File Page') not in result:
        assert False
    else:
        pass

def test_Image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Image Page') not in result:
        assert False
    else:
        pass

def test_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        '<form action=\'/submit\' method=\'GET\'>\r\n' and \
        'First Name: <input type=\'text\' name=\'firstname\'><br>\r\n' and \
        'Last Name: <input type=\'text\' name=\'lastname\'><br>\r\n' and \
        '<input type=\'submit\' name=\'submit\'>\r\n' and \
        '</form>') not in result:
        assert False
    else:
        pass

def test_submit():
    conn = FakeConnection("GET /submit?firstname=Eunbong&lastname=Yang&submit=Submit HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Hello Eunbong Yang!') not in result:
        assert False
    else:
        pass

def test_post_app():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "Content-Length: 31\r\n" + \
                          "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
                          "firstname=Eunbong&lastname=Yang\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if 'HTTP/1.0 200 OK' not in result:
        assert False
    else:
        pass

def test_post_multi():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "Content-Length: 187\r\n" + \
                          "Content-Type: multipart/form-data; boundary=AaB03x\r\n\r\n" + \
                          "--AaB03x\r\n" + \
                          "Content-Disposition: form-data; name=\"firstname\";" + \
                          " filename=\"firstname\"\r\n\r\n" + \
                          "Eunbong\r\n" + \
                          "--AaB03x\r\n" + \
                          "Content-Disposition: form-data; name=\"lastname\";" + \
                          " filename=\"lastname\"\r\n\r\n" + \
                          "Yang\r\n" + \
                          "--AaB03x\r\n" + \
                          "Content-Disposition: form-data; name=\"key\";" + \
                          " filename=\"key\"\r\n\r\n" + \
                          "value\r\n" + \
                          "--AaB03x--\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if 'HTTP/1.0 200 OK' not in result:
        assert False
    else:
        pass

def test_main():
    fakemodule = FakeSocketModule()

    success = False
    try:
        server.main(fakemodule)
    except AcceptCalledMultipleTimes:
        success = True
        pass

    assert success, "Something went wrong"

class AcceptCalledMultipleTimes(Exception):
    pass

class FakeSocketModule(object):
    def getfqdn(self):
        return "fakehost"

    def socket(self):
        return FakeConnection("")

class FakeConnection(object):
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False
        self.n_times_accept_called = 0

    def bind(self, param):
        (host, port) = param

    def listen(self, n):
        assert n == 5
        if n != 5:
            raise Exception("n should be five you dumby")

    def accept(self):
        if self.n_times_accept_called > 1:
            raise AcceptCalledMultipleTimes("stop calling accept, please")
        self.n_times_accept_called += 1
        
        c = FakeConnection("")
        return c, ("noclient", 32351)

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


##import server
##
##post_content_type = "Content-Type: application/x-www-form-urlencoded\r\n\r\n"
##
##class FakeConnection(object):
##    """
##    A fake connection class that mimics a real TCP socket for the purpose
##    of testing socket I/O.
##    """
##    def __init__(self, to_recv):
##        self.to_recv = to_recv
##        self.sent = ""
##        self.is_closed = False
##
##    def recv(self, n):
##        if n > len(self.to_recv):
##            r = self.to_recv
##            self.to_recv = ""
##            return r
##            
##        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
##        return r
##
##    def send(self, s):
##        self.sent += s
##
##    def close(self):
##        self.is_closed = True
##
### Test a basic GET call.
##
##def test_handle_connection_index():
##    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
##    msg = 'HTTP/1.0 200 OK\r\n'
##
##    server.handle_connection(conn, 80)
##
##    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)
##    
##def test_handle_connection_content():
##    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
##    msg = 'HTTP/1.0 200 OK\r\n'
##
##    server.handle_connection(conn, 80)
##
##    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)
##
##def test_handle_connection_file():
##    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
##    msg = 'HTTP/1.0 200 OK\r\n'
##
##    server.handle_connection(conn, 80)
##
##    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)
##
##def test_handle_connection_image():
##    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
##    msg = 'HTTP/1.0 200 OK\r\n'
##
##    server.handle_connection(conn, 80)
##
##    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)
##
##def test_get_form():
##    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
##    msg = 'HTTP/1.0 200 OK\r\n'
##
##    server.handle_connection(conn, 80)
##
##    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)
##
##def test_404():
##    conn = FakeConnection("GET /404 HTTP/1.0\r\n\r\n")
##    msg = 'HTTP/1.0 404 Not Found\r\n'
##
##    server.handle_connection(conn, 80)
##
##    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)
##
##def test_submit_get():
##    firstname = "Eunbong"
##    lastname = "Yang"
##    
##    conn = FakeConnection("GET /submit?firstname={0}&lastname={1} \
##                          HTTP/1.0\r\n\r\n".format(firstname, lastname))
##    msg = 'HTTP/1.0 200 OK\r\n'
##
##    server.handle_connection(conn, 80)
##
##    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)
##
##def test_submit_post_urlencoded():
##    firstname = "Eunbong"
##    lastname = "Yang"
##    name_info = "firstname={0}&lastname={1}\r\n".format(firstname, lastname)
##    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
##                          "Content-Length: 29\r\n" + \
##                          post_content_type + \
##                          name_info)
##    msg = 'HTTP/1.0 200 OK\r\n'
##
##    server.handle_connection(conn, 80)
##
##    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)
##
##def test_submit_post_multipart():
##    fake_info = "POST /submit HTTP/1.0\r\n" + \
##                "Content-Length: 374\r\n" + \
##                "Content-Type: multipart/form-data; " + \
##                "boundary=32452685f36942178a5f36fd94e34b63\r\n\r\n" + \
##                "--32452685f36942178a5f36fd94e34b63\r\n" + \
##                "Content-Disposition: form-data; name=\"lastname\";" + \
##                " filename=\"lastname\"\r\n\r\n" + \
##                "Yang\r\n" + \
##                "--32452685f36942178a5f36fd94e34b63\r\n" + \
##                "Content-Disposition: form-data; name=\"firstname\";" + \
##                " filename=\"firstname\"\r\n\r\n" + \
##                "Eunbong\r\n" + \
##                "--32452685f36942178a5f36fd94e34b63\r\n" + \
##                "Content-Disposition: form-data; name=\"key\";" + \
##                " filename=\"key\"\r\n\r\n" + \
##                "value\r\n" + \
##                "--32452685f36942178a5f36fd94e34b63--\r\n"
##    
##    conn = FakeConnection(fake_info)
##    
##    firstname = 'Eunbong'
##    lastname = 'Yang'
##    msg = 'HTTP/1.0 200 OK\r\n'
##
##    server.handle_connection(conn, 80)
##
##    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)
##
##def test_submit_post_404():
##    conn = FakeConnection("POST /asdf HTTP/1.0\r\n" + \
##                          "Content-Length: 0\r\n" + \
##                          post_content_type
##                         )
##    server.handle_connection(conn, 80)
##
##    msg = 'HTTP/1.0 404 Not Found\r\n'
##
##    assert conn.sent[:len(msg)] == msg, 'Got: %s' % (repr(conn.sent),)

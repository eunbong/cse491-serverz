#! /usr/bin/env python

import cgi
import jinja2
import os
import traceback
import urllib
from StringIO import StringIO
from urlparse import urlparse, parse_qs
from wsgiref.simple_server import make_server


def render_page(page, params):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    template = env.get_template(page)
    x = template.render(params).encode('latin-1', 'replace')
    return str(x)

# Get a list of all files in a directory
def get_contents(dir):
    list = []
    for file in os.listdir(dir):
        list.append(file)
    return list

def get_file(file_in):
    fp = open(file_in, 'rb')
    data = [fp.read()]
    fp.close
    return data

class MyApp(object):
    def __call__(self, environ, start_response):
        options = {'/'            : self.index,
                   '/content'     : self.content,
                   '/file'       : self.File,
                   '/image'      : self.Image,
                   '/form'        : self.form,
                   '/submit'      : self.submit  }

        path = environ['PATH_INFO']
        if path[:5] == '/text':
            return self.text(environ, start_response) 
        elif path[:5] == '/pics':
            return self.pics(environ, start_response) 
        page = options.get(path)

        if page is None:
            return self.error(environ, start_response)

        return page(environ, start_response)

    def error(self, environ, start_response):
        start_response('404 Not Found', [('Content-type', 'text/html')])
        return render_page('404NotFound.html','')

    def index(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return render_page('index.html','')

    def content(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return render_page('content.html','')

    def File(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        params = dict(names=get_contents('files'))
        return render_page('file.html', params)

    def Image(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        params = dict(names=get_contents('images'))
        return render_page('image.html', params)

    def form(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return render_page('form.html','')

    def submit(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        if method == 'GET':
            return self.handle_get(environ, start_response)
        else:
            return self.handle_post(environ, start_response)

    def handle_get(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        params = parse_qs(environ['QUERY_STRING'])
        return render_page('submit.html', params)

    def handle_post(self, environ, start_response):
        con_type = environ['CONTENT_TYPE']
        headers = {}
        params ={} 
        for k, v in environ.iteritems():
            headers['content-type'] = environ['CONTENT_TYPE']
            headers['content-length'] = environ['CONTENT_LENGTH']
            fs = cgi.FieldStorage(fp=environ['wsgi.input'], \
                                  headers=headers, environ=environ)
            params.update({x: [fs[x].value] for x in fs.keys()}) 
        start_response('200 OK', [('Content-type', con_type)])
        return render_page('submit.html', params)

    def text(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/plain')])
        text_file = './files/' + environ['PATH_INFO'][5:]
        return get_file(text_file)

    def pics(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'image/jpeg')])
        pic_file = './images/' + environ['PATH_INFO'][5:]
        return get_file(pic_file)

def make_app():
    return MyApp()


### encoding: utf-8
##
##import jinja2
##from urlparse import parse_qs
##import cgi
##from os import listdir
##from random import choice
##from StringIO import StringIO
##
### Helper functions
##def fileData(filename):
##    fp = open(filename, 'rb')
##    data = [fp.read()]
##    fp.close()
##    return data
##
##def index(env, **kwargs):
##    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
##
##    template = env.get_template('index.html')
##    data = [template.render(kwargs).encode('utf-8')]
##
##    return (response_headers, data)
##
##def content(env, **kwargs):
##    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
##
##    template = env.get_template('content.html')
##    data = [template.render(kwargs).encode('utf-8')]
##
##    return (response_headers, data)
##
##def serveImage(env, **kwargs):
##    response_headers = [('Content-type', 'image/jpeg')]
##
##    data = fileData(kwargs['path'][1:])
##
##    return (response_headers, data)
##
##def serveFile(env, **kwargs):
##    response_headers = [('Content-type', 'text/plain; charset="UTF-8"')]
##
##    data = fileData(kwargs['path'][1:])
##
##    return (response_headers, data)
##
##def File(env, **kwargs):
##    kwargs['path'] = '/files/'+choice(listdir('files'))
##    return serveFile(env, **kwargs)
##
##def Image(env, **kwargs):
##    kwargs['path'] = '/images/'+choice(listdir('images'))
##    print kwargs['path']
##    return serveFile(env, **kwargs)
##
##def form(env, **kwargs):
##    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
##
##    template = env.get_template('form.html')
##    data = [template.render(kwargs).encode('utf-8')]
##
##    return (response_headers, data)
##
##def submit(env, **kwargs):
##    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
##    
##    template = env.get_template('submit.html')
##    data = [template.render(kwargs).encode('utf-8')]
##    
##    return (response_headers, data)
##
##def fail(env, **kwargs):
##    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
##
##    # Select an amusing image to acompany
##    kwargs['img'] = './notFound/'+choice(listdir('notFound'))
##    
##    template = env.get_template('404NotFound.html')
##    data = [template.render(kwargs).encode('utf-8')]
##    
##    return (response_headers, data)
##
##def app(environ, start_response):
##    """A simple WSGI application which serves several pages 
##        and handles form data"""
##
##    # The dict of pages we know how to serve, and their corresponding templates
##    response = {
##                '/'        : index,      \
##                '/content' : content,    \
##                '/file'    : File,  \
##                '/image'   : Image, \
##                '/form'    : form,       \
##                '/submit'  : submit,     \
##                '404'      : fail,       \
##               }
##
##    # Manually add all other available pages/images
##    for page in listdir('notFound'):
##        response['/notFound/' + page] = serveImage
##    for page in listdir('images'):
##        response['/images/' + page] = serveImage
##    for page in listdir('files'):
##        response['/files/' + page] = serveFile
##
##    # Basic connection information and set up templates
##    loader = jinja2.FileSystemLoader('./templates')
##    env = jinja2.Environment(loader=loader)
##
##    # Set up template arguments from GET requests
##    qs = parse_qs(environ['QUERY_STRING']).iteritems()
##    # Flatten the list we get from parse_qs; just assume we want the 0th for now
##    args = {key : val[0] for key, val in qs}
##    # Add the path to the args; we'll use this for page titles and 404s
##    args['path'] = environ['PATH_INFO']
##
##    # Grab POST args if there are any
##    if environ['REQUEST_METHOD'] == 'POST':
##        # Re-parse the headers into a format field storage can use
##        # Dashes instead of underscores, all lowercased
##        headers = { 
##                    key[5:].lower().replace('_','-') : val \
##                    for key, val in environ.iteritems()    \
##                    if(key.startswith('HTTP'))
##                  }
##        # Pull in the non-HTTP variables that field storage needs manually
##        headers['content-type'] = environ['CONTENT_TYPE']
##        headers['content-length'] = environ['CONTENT_LENGTH']
##        # Create a field storage to process POST args
##
##        ## Bad hack to get around validator problem
##        if "multipart/form-data" in environ['CONTENT_TYPE']:
##            cLen = int(environ['CONTENT_LENGTH'])
##            data = environ['wsgi.input'].read(cLen)
##            environ['wsgi.input'] = StringIO(data)
##
##        fs = cgi.FieldStorage(fp=environ['wsgi.input'], \
##                                headers=headers, environ=environ)
##        # Add these new args to the existing set
##        args.update({key : fs[key].value for key in fs.keys()})
##
##    # Get all the arguments in unicode form for Jinja
##    args = {
##            key.decode('utf-8') : val.decode('utf-8') \
##            for key, val in args.iteritems()
##           }
##    
##    # Check if we got a path to an existing page
##    if environ['PATH_INFO'] in response:
##        # If we have that page, serve it with a 200 OK
##        status = '200 OK'
##        path = environ['PATH_INFO']
##        
##    else:
##        # If we did not, redirect to the 404 page, with appropriate status
##        status = '404 Not Found'
##        path = '404'
##
##    args['path'] = path
##    response_headers, data = response[path](env, **args)
##
##    # Return the page and status code
##    # Page is first encoded to bytes from unicode for compatibility
##    start_response(status, response_headers)
##    return data
##
##def make_app():
##    """Wrapper function; returns the app function above to a WSGI server"""
##    return app

##def app(environ, start_response):
##    # The dict of pages we know how to get to
##    response = {
##                '/' : 'index.html', \
##                '/content' : 'content.html', \
##                '/file' : 'file.html', \
##                '/image' : 'image.html', \
##                '/form' : 'form.html', \
##                '/submit' : 'submit.html', \
##               }
##
##    # Basic connection information and set up templates
##    loader = jinja2.FileSystemLoader('./templates')
##    env = jinja2.Environment(loader=loader)
##    response_headers = [('Content-type', 'text/html')]
##
##    # Check if we got a path to an existing page
##    if environ['PATH_INFO'] in response:
##        status = '200 OK'
##        template = env.get_template(response[environ['PATH_INFO']])
##    else:
##        status = '404 Not Found'
##        template = env.get_template('404NotFound.html')
##
##    # Set up template arguments
##    x = parse_qs(environ['QUERY_STRING']).iteritems()
##    args = {k : v[0] for k,v in x}
##    args['path'] = environ['PATH_INFO']
##
##    # Grab POST args if there are any
##    if environ['REQUEST_METHOD'] == 'POST':
##        headers = {k[5:].lower().replace('_','-') : v \
##                    for k,v in environ.iteritems() if(k.startswith('HTTP'))}
##        headers['content-type'] = environ['CONTENT_TYPE']
##        headers['content-length'] = environ['CONTENT_LENGTH']
##        fs = cgi.FieldStorage(fp=environ['wsgi.input'], \
##                                headers=headers, environ=environ)
##        args.update({x : fs[x].value for x in fs.keys()})
##
##    args = {unicode(k, "utf-8") : unicode(v, "utf-8") for k,v in args.iteritems()}
##    print args
##    # Return the page
##    start_response(status, response_headers)
##    return [bytes(template.render(args))]
##
##def make_app():
##    return app

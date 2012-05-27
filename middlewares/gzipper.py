#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A WSGI middleware application that automatically gzips output
    to the client.
    Before doing any gzipping, it first checks the environ to see if
    the client can even support gzipped output. If not, it immediately
    drops out.
    It automatically modifies the headers to include the proper values
    for the 'Accept-Encoding' and 'Vary' headers.

    Example of use:

        from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

        def test_app(environ, start_response):
            status = '200 OK'
            headers = [('content-type', 'text/html')]
            start_response(status, headers)

            return ['Hello gzipped world!']

        app = Gzipper(test_app, compresslevel=8)
        httpd = WSGIServer(('', 8080), WSGIRequestHandler)
        httpd.set_app(app)
        httpd.serve_forever()

"""
from gzip import GzipFile
import cStringIO

__version__ = (1, 0)
__author__ = "Evan Fosmark"


def gzip_string(string, compression_level):
    """ The `gzip` module didn't provide a way to gzip just a string.
        Had to hack together this. I know, it isn't pretty.
    """
    fake_file = cStringIO.StringIO()
    gz_file = GzipFile(None, 'wb', compression_level, fake_file)
    gz_file.write(string)
    gz_file.close()
    return fake_file.getvalue()


def parse_encoding_header(header):
    """ Break up the `HTTP_ACCEPT_ENCODING` header into a dict of
        the form, {'encoding-name':qvalue}.
    """
    encodings = {'identity': 1.0}

    for encoding in header.split(","):
        if(encoding.find(";") > -1):
            encoding, qvalue = encoding.split(";")
            encoding = encoding.strip()
            qvalue = qvalue.split('=', 1)[1]
            if(qvalue != ""):
                encodings[encoding] = float(qvalue)
            else:
                encodings[encoding] = 1
        else:
            encodings[encoding] = 1
    return encodings


def client_wants_gzip(accept_encoding_header):
    """ Check to see if the client can accept gzipped output, and whether
        or not it is even the preferred method. If `identity` is higher, then
        no gzipping should occur.
    """
    encodings = parse_encoding_header(accept_encoding_header)

    # Do the actual comparisons
    if('gzip' in encodings):
        return encodings['gzip'] >= encodings['identity']

    elif('*' in encodings):
        return encodings['*'] >= encodings['identity']

    else:
        return False


class Gzipper(object):
    """ WSGI middleware to wrap around and gzip all output.
        This automatically adds the content-encoding header.
    """
    def __init__(self, app, compresslevel=6):
        self.app = app
        self.compresslevel = compresslevel

    def __call__(self, environ, start_response):
        """ Do the actual work. If the host doesn't support gzip as a
            proper encoding, then simply pass over to the next app on
            the wsgi stack.
        """
        accept_encoding_header = environ.get("HTTP_ACCEPT_ENCODING", "")
        if(not client_wants_gzip(accept_encoding_header)):
                return self.app(environ, start_response)

        def _start_response(status, headers, *args, **kwargs):
            """ Wrapper around the original `start_response` function.
                The sole purpose being to add the proper headers automatically.
            """
            headers.append(("Content-Encoding", "gzip"))
            headers.append(("Vary", "Accept-Encoding"))
            return start_response(status, headers, *args, **kwargs)

        data = "".join(self.app(environ, _start_response))
        return [gzip_string(data, self.compresslevel)]

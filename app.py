#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime
import hashlib
import flask
from flask import Flask, render_template, request
from helpers.decorators import cached
from helpers.pil import pil_image, serve_pil_image
from helpers.converters import ColorConverter, ImgSizeConverter
try:
    from raven.contrib.flask import Sentry
except ImportError:
    pass


app = Flask(__name__)
# Custom converter for matching hexadecimal colors
app.url_map.converters['color'] = ColorConverter
# Custom converter for not having an image > 4000px
app.url_map.converters['imgs'] = ImgSizeConverter
# Generate Last-Modified timestamp
launch_date = datetime.datetime.now()


@app.route('/')
@cached(60, 'index')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/<imgs:width>/')
@app.route('/<imgs:width>/<color:bgd>/')
@app.route('/<imgs:width>/<color:bgd>/<color:fgd>/')
@app.route('/<imgs:width>x<imgs:height>/')
@app.route('/<imgs:width>x<imgs:height>/<color:bgd>/')
@app.route('/<imgs:width>x<imgs:height>/<color:bgd>/<color:fgd>/')
def placeholder(width, height=None, bgd="cccccc", fgd="909090"):
    """This endpoint generates the placeholder itself, based on arguments.
    If the height is missing, just make the image square.
    """
    height = height or width
    # get optional caption, default is width X height
    # fakeimg.pl/400x400/?text=whosmad
    txt = request.args.get('text', "{0} x {1}".format(width, height))
    # grab the font, default is yanone
    # fakeimg.pl/400x400/?font=lobster
    font = request.args.get('font', 'yanone')
    # retina mode, just make the image twice bigger
    if request.args.get('retina'):
        width, height = [x * 2 for x in [width, height]]
    # processing image
    im = pil_image(width, height, bgd, fgd, txt, font)
    return serve_pil_image(im)


# caching stuff
@app.before_request
def handle_cache():
    """if resource is the same, return 304"""
    # we test Etag first, as it's a strong validator
    etag = hashlib.sha1(request.url).hexdigest()
    if request.headers.get('If-None-Match') == etag:
        return flask.Response(status=304)
    # then we try with Last-Modified
    if request.headers.get('If-Modified-Since') == str(launch_date):
        return flask.Response(status=304)


@app.after_request
def add_header(response):
    """Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 hours. Should be served by
    Varnish servers.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public,max-age=36000'
    response.headers['Last-Modified'] = launch_date
    response.headers['Etag'] = hashlib.sha1(request.url).hexdigest()
    return response


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = u'{0}.txt'.format(file_name)
    return app.send_static_file(file_dot_text)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Sentry
SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    app.config['SENTRY_DSN'] = SENTRY_DSN
    sentry = Sentry(app)


if __name__ == '__main__':
    # app.debug = True
    port = int(os.environ.get('PORT', 8000))
    # logging
    if not app.debug:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=port)

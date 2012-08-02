#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
from flask import Flask, render_template, abort, request
from helpers.decorators import cached
from helpers.pil import pil_image, serve_pil_image
from helpers.colors_converter import ColorConverter


app = Flask(__name__)
# Custom converter for matching hexadecimal colors
app.url_map.converters['color'] = ColorConverter


@app.route('/')
@cached(60, 'index')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/<int:width>/')
@app.route('/<int:width>x<int:height>/')
@app.route('/<int:width>x<int:height>/<color:color_bgd>/')
@app.route('/<int:width>x<int:height>/<color:color_bgd>/<color:color_fgd>/')
def placeholder(width, height=None, color_bgd="cccccc", color_fgd="909090"):
    if width is not None:
        if height is None:
            height = width
        # check size limit
        if width > 4000 or height > 4000:
            abort(404)
        # get optionnal caption
        txt = request.args.get('text', None)
        # lobster for the shitty designers
        lobster = request.args.get('lobster', None)
        # processing image
        im = pil_image(width, height, color_bgd, color_fgd, txt, lobster)
        return serve_pil_image(im)
    abort(404)


# basic stuff
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 hours. Should be served by
    Varnish servers.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=36000'
    return response


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/apple-touch-icon.png')
@app.route('/apple-touch-icon<format>.png')
def apple_touch(format=""):
    """Shitty logo Apple"""
    file = 'apple-touch-icon%s.png' % format
    return app.send_static_file(file)


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = '%s.txt' % file_name
    return app.send_static_file(file_dot_text)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # app.debug = True
    # Gzipping, not worth it on my free Heroku cedar
    # Cloudflare will do it for me.
    # app.wsgi_app = Gzipper(app.wsgi_app, compresslevel=6)
    port = int(os.environ.get('PORT', 5000))
    # logging
    if not app.debug:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)


    app.run(host='0.0.0.0', port=port)


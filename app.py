#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
from flask import Flask, render_template, request
from helpers.decorators import cached
from helpers.pil import pil_image, serve_pil_image
from helpers.converters import ColorConverter, ImgSizeConverter


app = Flask(__name__)
# Custom converter for matching hexadecimal colors
app.url_map.converters['color'] = ColorConverter
# Custom converter for not having an image > 4000px
app.url_map.converters['imgs'] = ImgSizeConverter


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
    """
    This endpoint generates the placeholder itself, based on arguments.
    If the height is missing, just make the image square.
    """
    if height is None:
        height = width
    # get optional caption
    txt = request.args.get('text', None)
    # lobster for the shitty designers
    # fakeimg.pl/400x400/?font=lobster
    font = request.args.get('font', None)
    # processing image
    im = pil_image(width, height, bgd, fgd, txt, font)
    return serve_pil_image(im)


# basic stuff
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 hours. Should be served by
    Varnish servers.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public,max-age=36000'
    return response


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


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
    port = int(os.environ.get('PORT', 5000))
    # logging
    if not app.debug:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=port)

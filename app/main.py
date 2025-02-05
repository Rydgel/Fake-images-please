import os
import sys
import logging
import datetime
import hashlib
import flask
from flask import Flask, render_template, request, make_response, send_file
from helpers.fakeimg import FakeImg
from helpers.converters import ColorConverter, ImgSizeConverter, AlphaConverter


app = Flask(__name__)
app.url_map.strict_slashes = False
# Custom converter for matching hexadecimal colors
app.url_map.converters['c'] = ColorConverter
# Custom converter for not having an image > 4000px
app.url_map.converters['i'] = ImgSizeConverter
app.url_map.converters['a'] = AlphaConverter
# Generate Last-Modified timestamp
launch_date = datetime.datetime.now()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', now=datetime.datetime.utcnow())


@app.route('/<i:width>/')
@app.route('/<i:width>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>/<c:bgd>/')
@app.route('/<i:width>/<c:bgd>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>/<c:bgd>,<a:alphabgd>/')
@app.route('/<i:width>/<c:bgd>,<a:alphabgd>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>/<c:bgd>/<c:fgd>/')
@app.route('/<i:width>/<c:bgd>/<c:fgd>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>/<c:bgd>,<a:alphabgd>/<c:fgd>/')
@app.route('/<i:width>/<c:bgd>,<a:alphabgd>/<c:fgd>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>/<c:bgd>/<c:fgd>,<a:alphafgd>/')
@app.route('/<i:width>/<c:bgd>/<c:fgd>,<a:alphafgd>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>/<c:bgd>,<a:alphabgd>/<c:fgd>,<a:alphafgd>/')
@app.route('/<i:width>/<c:bgd>,<a:alphabgd>/<c:fgd>,<a:alphafgd>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>x<i:height>/')
@app.route('/<i:width>x<i:height>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>x<i:height>/<c:bgd>/')
@app.route('/<i:width>x<i:height>/<c:bgd>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>x<i:height>/<c:bgd>,<a:alphabgd>/')
@app.route('/<i:width>x<i:height>/<c:bgd>,<a:alphabgd>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>x<i:height>/<c:bgd>/<c:fgd>/')
@app.route('/<i:width>x<i:height>/<c:bgd>/<c:fgd>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>x<i:height>/<c:bgd>,<a:alphabgd>/<c:fgd>/')
@app.route('/<i:width>x<i:height>/<c:bgd>,<a:alphabgd>/<c:fgd>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>x<i:height>/<c:bgd>/<c:fgd>,<a:alphafgd>/')
@app.route('/<i:width>x<i:height>/<c:bgd>/<c:fgd>,<a:alphafgd>/<image_name>.<any("png", "webp"):image_type>')

@app.route('/<i:width>x<i:height>/<c:bgd>,<a:alphabgd>/<c:fgd>,<a:alphafgd>/')
@app.route('/<i:width>x<i:height>/<c:bgd>,<a:alphabgd>/<c:fgd>,<a:alphafgd>/<image_name>.<any("png", "webp"):image_type>')

def placeholder(width, height=None,
                bgd="cccccc", fgd="909090",
                alphabgd=255, alphafgd=255, image_name="", image_type="png"):
    """This endpoint generates the placeholder itself, based on arguments.
    If the height is missing, just make the image square.
    """
    # processing image
    args = {
        "width": width,
        "height": height or width,
        "background_color": bgd,
        "alpha_background": alphabgd,
        "foreground_color": fgd,
        "alpha_foreground": alphafgd,
        "text": request.args.get('text'),
        "font_name": request.args.get('font'),
        "font_size": request.args.get('font_size'),
        "retina": "retina" in request.args,
        "image_type": image_type,
    }
    image = FakeImg(**args)
    response = make_response(send_file(image.raw, mimetype=image.mimetype, etag=False))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# caching stuff
@app.before_request
def handle_cache():
    """if resource is the same, return 304"""
    # we test Etag first, as it's a strong validator
    url_bytes = request.url.encode('utf-8')
    etag = hashlib.sha1(url_bytes).hexdigest()
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
    url_bytes = request.url.encode('utf-8')
    response.headers['Etag'] = hashlib.sha1(url_bytes).hexdigest()
    return response


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    return app.send_static_file(f"{file_name}.txt")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # app.debug = True
    port = int(os.environ.get('PORT', 8001))
    # logging
    if not app.debug:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=port)

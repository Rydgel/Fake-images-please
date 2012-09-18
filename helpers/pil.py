#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import StringIO
from PIL import Image, ImageDraw, ImageFont
from flask import send_file


def pil_image(width, height, color_bgd, color_fgd, txt=None, font=None):
    """
    Image creation using Pillow (PIL fork)
    """
    size = (width, height)
    hex_color_background = "#%s" % color_bgd
    hex_color_foreground = "#%s" % color_fgd
    im = Image.new("RGB", size, hex_color_background)
    # Draw on the image
    draw = ImageDraw.Draw(im)

    font_size = _calculate_font_size(width, height)
    font = _choose_font(font_size, font)

    w, h = font.getsize(txt)
    text_coord = ((width - w) / 2, (height - h) / 2)
    draw.text(text_coord, txt, fill=hex_color_foreground, font=font)

    del draw
    return im


def serve_pil_image(im):
    """
    Serve the image created directly on the fly
    """
    img_io = StringIO.StringIO()
    im.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


def _calculate_font_size(width, height):
    min_side = min(width, height)
    return int(min_side / 4)


def _choose_font(font_size, font=None):
    """
    For those who like Lobster...
    """
    dirname = os.path.dirname
    font_path = '%s/font/%s.otf' % (dirname(dirname(__file__)), font)
    try:
        return ImageFont.truetype(font_path, font_size)
    except IOError, e:
        # font not found: fallback
        return _choose_font(font_size, 'yanone')

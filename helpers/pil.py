#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -e git+git://github.com/fuzion/pil-2009-raclette.git#egg=PIL
import os
import cStringIO
from PIL import Image, ImageDraw, ImageFont
from flask import send_file

dirname = os.path.dirname
FONT_PATH = dirname(dirname(__file__))


def pil_image(width, height, color_bgd, color_fgd, txt=None):
	size = (width, height)
	hex_color_background = "#" + color_bgd
	hex_color_foreground = "#" + color_fgd
	im = Image.new("RGB", size, hex_color_background)
	# Draw on the image
	draw = ImageDraw.Draw(im)
	
	if txt is None:
		# regular text: width x height
		txt = "%d x %d"  % (width, height)
	
	font_size = _calculate_font_size(width, height)
	font = ImageFont.truetype(FONT_PATH + '/font/YanoneKaffeesatz-Bold.otf', font_size)
	w, h = font.getsize(txt)
	text_coord = ( (width-w)/2, (height-h)/2 )
	draw.text(text_coord, txt, fill=hex_color_foreground, font=font)

	del draw
	return im


def _calculate_font_size(width, height):
	min_side = min(width, height)
	return int(min_side / 5)


def serve_pil_image(im):
    img_io = cStringIO.StringIO()
    im.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

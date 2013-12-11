# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from werkzeug.routing import BaseConverter, IntegerConverter


class ColorConverter(BaseConverter):
    """This converter is used to be sure that the color setted in the URL is a
    valid hexadecimal one.
    """
    def __init__(self, url_map):
        super(ColorConverter, self).__init__(url_map)
        self.regex = "([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})"


class ImgSizeConverter(IntegerConverter):
    """This converter is used to be sure that the requested image size is not
    too big
    """
    def __init__(self, url_map):
        super(ImgSizeConverter, self).__init__(url_map, min=1, max=4000)


class AlphaConverter(IntegerConverter):
    """This converter was made to simplify the routes"""
    def __init__(self, url_map):
        super(AlphaConverter, self).__init__(url_map, min=0, max=255)


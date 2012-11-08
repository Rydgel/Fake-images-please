#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

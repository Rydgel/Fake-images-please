#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.routing import BaseConverter, IntegerConverter


class ColorConverter(BaseConverter):

    def __init__(self, url_map):
        super(ColorConverter, self).__init__(url_map)
        self.regex = "([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})"


class ImgSizeConverter(IntegerConverter):

    def __init__(self, url_map):
        super(ImgSizeConverter, self).__init__(url_map, min=1, max=4000)

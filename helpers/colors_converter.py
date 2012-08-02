#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from werkzeug.routing import BaseConverter


class ColorConverter(BaseConverter):

    def __init__(self, url_map):
        super(ColorConverter, self).__init__(url_map)
        self.regex = "([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})"

 
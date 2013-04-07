#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import unittest
from app import app
from PIL import Image
import StringIO


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def _open_image(self, image_data):
        strio = StringIO.StringIO()
        strio.write(image_data)
        strio.seek(0)
        return Image.open(strio)

    # Routes

    def testIndex(self):
        r = self.app.get('/')
        self.assertEquals(r.status_code, 200)

    def test404(self):
        r = self.app.get('/this-does-not-exist-bitch')
        self.assertEquals(r.status_code, 404)

    def testHeaders(self):
        headers = self.app.get('/').headers
        self.assertEquals(headers['X-UA-Compatible'], 'IE=Edge,chrome=1')
        self.assertEquals(headers['Cache-Control'], 'public,max-age=36000')

    def testFavicon(self):
        r = self.app.get('/favicon.ico')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.mimetype, 'image/x-icon')

    def testRobotsTxt(self):
        r = self.app.get('/robots.txt')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.mimetype, 'text/plain')

    def testHumansTxt(self):
        r = self.app.get('/humans.txt')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.mimetype, 'text/plain')

    def testTrailingSlash(self):
        # redirected to /100/
        r = self.app.get('/100')
        self.assertEquals(r.status_code, 301)

    def testPlaceholder1(self):
        r = self.app.get('/300/')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.mimetype, 'image/png')
        img = self._open_image(r.data)
        width, height = img.size
        self.assertEquals(width, 300)
        self.assertEquals(height, 300)

        r = self.app.get('/5000/')
        self.assertEquals(r.status_code, 404)

    def testPlaceholder2(self):
        r = self.app.get('/200x100/')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.mimetype, 'image/png')
        img = self._open_image(r.data)
        width, height = img.size
        self.assertEquals(width, 200)
        self.assertEquals(height, 100)

        r = self.app.get('/4005x300/')
        self.assertEquals(r.status_code, 404)

        r = self.app.get('/200x4050/')
        self.assertEquals(r.status_code, 404)

    def testPlaceholder3(self):
        r = self.app.get('/200x100/CCCCCC/')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.mimetype, 'image/png')
        img = self._open_image(r.data)
        width, height = img.size
        self.assertEquals(width, 200)
        self.assertEquals(height, 100)

        r = self.app.get('/200x100/prout/')
        self.assertEquals(r.status_code, 404)

    def testPlaceholder4(self):
        r = self.app.get('/200x100/eee/000/')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.mimetype, 'image/png')
        img = self._open_image(r.data)
        width, height = img.size
        self.assertEquals(width, 200)
        self.assertEquals(height, 100)

        r = self.app.get('/200x100/fff/ee')
        self.assertEquals(r.status_code, 404)

        r = self.app.get('/200x100/eeeeeee/fff')
        self.assertEquals(r.status_code, 404)

    def testRetina(self):
        r = self.app.get('/200x100/eee/000/?retina=1')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.mimetype, 'image/png')
        img = self._open_image(r.data)
        width, height = img.size
        self.assertEquals(width, 400)
        self.assertEquals(height, 200)

    def testFontsize(self):
        r = self.app.get('/200x100/eee/000/?font_size=1')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.mimetype, 'image/png')
        img = self._open_image(r.data)
        width, height = img.size
        self.assertEquals(width, 200)
        self.assertEquals(height, 100)

        # Make it work with wrong value (ie. not crash)

        r = self.app.get('/200x100/eee/000/?font_size=0')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.mimetype, 'image/png')
        img = self._open_image(r.data)
        width, height = img.size
        self.assertEquals(width, 200)
        self.assertEquals(height, 100)

        r = self.app.get('/200x100/eee/000/?font_size=-1')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.mimetype, 'image/png')
        img = self._open_image(r.data)
        width, height = img.size
        self.assertEquals(width, 200)
        self.assertEquals(height, 100)

if __name__ == '__main__':
    unittest.main()

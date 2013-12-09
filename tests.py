#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import unittest
from app import app
from PIL import Image
from io import BytesIO


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def _open_image(self, image_data):
        strio = BytesIO()
        strio.write(image_data)
        strio.seek(0)
        return Image.open(strio)

    # Routes

    def testIndex(self):
        with self.app.get('/') as r:
            self.assertEqual(r.status_code, 200)

    def test404(self):
        with self.app.get('/this-does-not-exist-bitch') as r:
            self.assertEqual(r.status_code, 404)

    def testHeaders(self):
        with self.app.get('/') as r:
            headers = r.headers
            self.assertEqual(headers['X-UA-Compatible'], 'IE=Edge,chrome=1')
            self.assertEqual(headers['Cache-Control'], 'public,max-age=36000')

    def testFavicon(self):
        with self.app.get('/favicon.ico') as r:
            self.assertEqual(r.status_code, 200)

    def testRobotsTxt(self):
        with self.app.get('/robots.txt') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'text/plain')

    def testHumansTxt(self):
        with self.app.get('/humans.txt') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'text/plain')

    def testTrailingSlash(self):
        # redirected to /100/
        with self.app.get('/100') as r:
            self.assertEqual(r.status_code, 301)

    def testPlaceholder1(self):
        with self.app.get('/300/') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 300)
            self.assertEqual(height, 300)

        with self.app.get('/5000/') as r:
            self.assertEqual(r.status_code, 404)

    def testPlaceholder2(self):
        with self.app.get('/200x100/') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 200)
            self.assertEqual(height, 100)

        with self.app.get('/4005x300/') as r:
            self.assertEqual(r.status_code, 404)

        with self.app.get('/200x4050/') as r:
            self.assertEqual(r.status_code, 404)

    def testPlaceholder3(self):
        with self.app.get('/200x100/CCCCCC/') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 200)
            self.assertEqual(height, 100)

        with self.app.get('/200x100/CCCCCC,50/') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 200)
            self.assertEqual(height, 100)

        with self.app.get('/200x100/prout/') as r:
            self.assertEqual(r.status_code, 404)

        with self.app.get('/200x100/CCCCCC,5123/') as r:
            self.assertEqual(r.status_code, 404)

    def testPlaceholder4(self):
        with self.app.get('/200x100/eee/000/') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 200)
            self.assertEqual(height, 100)

        with self.app.get('/200x100/eee,10/000/') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 200)
            self.assertEqual(height, 100)

        with self.app.get('/200x100/eee/000,25/') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 200)
            self.assertEqual(height, 100)

        with self.app.get('/200x100/eee,15/000,15/') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 200)
            self.assertEqual(height, 100)

        with self.app.get('/200x100/fff/ee/') as r:
            self.assertEqual(r.status_code, 404)

        with self.app.get('/200x100/eee,25555/000/') as r:
            self.assertEqual(r.status_code, 404)

        with self.app.get('/200x100/eee/000,b/') as r:
            self.assertEqual(r.status_code, 404)

        with self.app.get('/200x100/eee,458/000,2555/') as r:
            self.assertEqual(r.status_code, 404)

    def testRetina(self):
        with self.app.get('/200x100/eee/000/?retina=1') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 400)
            self.assertEqual(height, 200)

        with self.app.get('/200x100/eee,10/000,10/?retina=1') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 400)
            self.assertEqual(height, 200)

    def testFontsize(self):
        with self.app.get('/200x100/eee/000/?font_size=1') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 200)
            self.assertEqual(height, 100)

        # Make it work with wrong value (ie. not crash)

        with self.app.get('/200x100/eee/000/?font_size=0') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 200)
            self.assertEqual(height, 100)

        with self.app.get('/200x100/eee/000/?font_size=-1') as r:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/png')
            img = self._open_image(r.data)
            width, height = img.size
            self.assertEqual(width, 200)
            self.assertEqual(height, 100)

if __name__ == '__main__':
    unittest.main()

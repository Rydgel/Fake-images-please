# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, division
import os
import StringIO
from PIL import Image, ImageDraw, ImageFont


class FakeImg():
    """A Fake Image.

    This class uses PIL to create an image based on passed parameters.

    Attributes:
        pil_image (PIL.Image.Image): PIL object.
        raw (str): Real image in PNG format.
    """
    def __init__(self, width, height, background_color, foreground_color,
                 text=None,
                 font_name=None,
                 font_size=None,
                 retina=False):
        """Init FakeImg with parameters.

        Args:
            width (int): The width of the image.
            height (int): The height of the image.
            background_color (str): The background color of the image. It
                should be in web hexadecimal format.
                Example: #FFF, #123456.
            foreground_color (str): The text color of the image. It should be
                in web hexadecimal format.
                Example: #FFF, #123456.
            text (str): Optional. The actual text which will be drawn on the
                image.
                Default: "{0} x {1}".format(width, height)
            font_name (str): Optional. The font name to use.
                Default: "yanone".
                Fallback to "yanone" if font not found.
            font_size (int): Optional. The font size to use.
                Default value is calculated based on the image dimension.
            retina (bool): Optional. Wether to use retina display or not.
                It basically just multiplies dimension of the image by 2.
        """
        if retina:
            self.width, self.height = [x * 2 for x in [width, height]]
        else:
            self.width, self.height = width, height
        self.background_color = "#{0}".format(background_color)
        self.foreground_color = "#{0}".format(foreground_color)
        self.text = text or "{0} x {1}".format(width, height)
        self.font_name = font_name or "yanone"
        try:
            if int(font_size) > 0:
                self.font_size = int(font_size)
            else:
                raise ValueError
        except (ValueError, TypeError):
            self.font_size = self._calculate_font_size()
        self.font = self._choose_font()
        self.pil_image = self._draw()

    @property
    def raw(self):
        """Create the image on memory and return it"""
        img_io = StringIO.StringIO()
        self.pil_image.save(img_io, 'PNG')
        img_io.seek(0)
        return img_io

    def _calculate_font_size(self):
        min_side = min(self.width, self.height)
        return int(min_side / 4)

    def _choose_font(self):
        """Choosing a font, the fallback is Yanone"""
        font_folder = os.path.dirname(os.path.dirname(__file__))
        font_path = '{0}/font/{1}.otf'.format(font_folder, self.font_name)
        try:
            return ImageFont.truetype(font_path, self.font_size)
        except IOError:
            # font not found: fallback
            self.font_name = "yanone"
            return self._choose_font()

    def _draw(self):
        """Image creation using Pillow (PIL fork)"""
        size = (self.width, self.height)
        image = Image.new("RGB", size, self.background_color)
        # Draw on the image
        draw = ImageDraw.Draw(image)

        text_width, text_height = self.font.getsize(self.text)
        text_coord = ((self.width - text_width) / 2,
                      (self.height - text_height) / 2)

        draw.text(text_coord, self.text,
                  fill=self.foreground_color, font=self.font)

        del draw

        return image

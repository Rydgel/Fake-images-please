import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji


class FakeImg:
    """A Fake Image.

    This class uses PIL to create an image based on passed parameters.

    Attributes:
        pil_image (PIL.Image.Image): PIL object.
        raw (str): Real image in PNG format.
    """
    def __init__(self, width, height, background_color, foreground_color, alpha_background, alpha_foreground, image_type,
                 text=None, font_name=None, font_size=None, retina=False):
        """Init FakeImg with parameters.

        Args:
            width (int): The width of the image.
            height (int): The height of the image.
            background_color (str): The background color of the image. It should be in web hexadecimal format.
                Example: #FFF, #123456.
            alpha_background (int): Alpha value of the background color.
            foreground_color (str): The text color of the image. It should be in web hexadecimal format.
                Example: #FFF, #123456.
            alpha_foreground (int): Alpha value of the foreground color.
            image_type (string): The image type which can be "png" or "webp".
            text (str): Optional. The actual text which will be drawn on the image.
                Default: f"{width} x {height}"
            font_name (str): Optional. The font name to use.
                Default: "yanone".
                Fallback to "yanone" if font not found.
            font_size (int): Optional. The font size to use. Default value is calculated based on the image dimension.
            retina (bool): Optional. Wether to use retina display or not. It basically just multiplies dimension of
            the image by 2.
        """
        if retina:
            self.width, self.height = [x * 2 for x in [width, height]]
        else:
            self.width, self.height = width, height
        self.background_color = f"#{background_color}"
        self.alpha_background = alpha_background
        self.foreground_color = f"#{foreground_color}"
        self.alpha_foreground = alpha_foreground
        self.image_type = image_type
        self.text = text or f"{width} x {height}"
        self.font_name = font_name or "yanone"
        try:
            if int(font_size) > 0:
                if retina:
                    # scaling font at retina display
                    self.font_size = 2 * int(font_size)
                else:
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
        img_io = BytesIO()
        self.pil_image.save(img_io, self.image_type.upper())
        img_io.seek(0)
        return img_io

    @property
    def mimetype(self):
        return "image/{image_type}".format(image_type = self.image_type)

    def _calculate_font_size(self):
        min_side = min(self.width, self.height)
        return int(min_side / 4)

    def _choose_font(self):
        """Choosing a font, the fallback is Yanone"""
        try:
            font_path = self._font_path_from_name()
            return ImageFont.truetype(font_path, self.font_size)
        except IOError:
            # font not found: fallback
            self.font_name = "yanone"
            return self._choose_font()

    @staticmethod
    def _hex_to_int(hex_string):
        return int(hex_string, 16)

    def _hex_alpha_to_rgba(self, hex_color, alpha):
        """Convert hexadecimal + alpha value to a rgba tuple"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([v * 2 for v in list(hex_color)])

        red = self._hex_to_int(hex_color[0:2])
        green = self._hex_to_int(hex_color[2:4])
        blue = self._hex_to_int(hex_color[4:6])

        return red, green, blue, alpha

    def _font_path_from_name(self):
        font_folder = os.path.dirname(os.path.dirname(__file__))
        if self.font_name == "bebas":
            return f"{font_folder}/font/bebas.otf"
        elif self.font_name == "lobster":
            return f"{font_folder}/font/lobster.otf"
        elif self.font_name == "museo":
            return f"{font_folder}/font/museo.otf"
        elif self.font_name == "noto":
            return f"{font_folder}/font/noto.ttc"
        elif self.font_name == "noto-sans":
            return f"{font_folder}/font/noto-sans.otf"
        elif self.font_name == "noto-serif":
            return f"{font_folder}/font/noto-serif.otf"
        else:
            return f"{font_folder}/font/yanone.otf"

    def _draw(self):
        """Image creation using Pillow (PIL fork)"""
        size = (self.width, self.height)

        rgba_background = self._hex_alpha_to_rgba(self.background_color, self.alpha_background)

        image = Image.new("RGBA", size, rgba_background)
        draw = Pilmoji(image)

        if "\n" in self.text:
            (_, top, _, bottom) = self.font.getbbox(self.text)
            y_offset = bottom - top
        else:
            y_offset = 0

        (text_width, text_height) = draw.getsize(self.text, font=self.font)
        text_coord_x = (self.width - text_width) // 2
        text_coord_y = (self.height - text_height - y_offset) // 2
        text_coord = (text_coord_x, text_coord_y)

        rgba_foreground = self._hex_alpha_to_rgba(self.foreground_color, self.alpha_foreground)

        draw.text(text_coord, self.text, fill=rgba_foreground, font=self.font, align="center", emoji_position_offset=(0, 10))

        del draw

        return image

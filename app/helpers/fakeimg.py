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
                 text=None, font_name=None, font_size=None, retina=False, corner_radius=None, corner_radii=None):
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
            retina (bool): Optional. Whether to use retina display or not. It basically just multiplies dimension of
            the image by 2.
            corner_radius (int): Optional. Uniform radius for all corners in pixels.
            corner_radii (tuple): Optional. Tuple of 4 integers for custom corner radii (top_left, top_right, bottom_right, bottom_left).
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
        
        # Handle corner radius parameters
        if corner_radii:
            self.corner_radii = corner_radii
        elif corner_radius is not None:
            self.corner_radii = (corner_radius,) * 4
        else:
            self.corner_radii = None
            
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
        
        # Create a transparent base image
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        
        # Create a mask for rounded corners if needed
        if self.corner_radii:
            mask = Image.new("L", size, 0)
            draw_mask = ImageDraw.Draw(mask)
            
            # Draw rounded rectangle on the mask
            rect = [(0, 0), (self.width - 1, self.height - 1)]
            if len(set(self.corner_radii)) == 1:
                # All corners have the same radius
                draw_mask.rounded_rectangle(rect, radius=self.corner_radii[0], fill=255)
            else:
                # Custom radii for each corner
                # We need to draw multiple arcs and lines to create the rounded rectangle
                tl, tr, br, bl = self.corner_radii  # top-left, top-right, bottom-right, bottom-left
                
                # Start with a filled rectangle
                draw_mask.rectangle(rect, fill=255)
                
                # Draw corner arcs with custom radii
                if tl > 0:  # Top-left
                    draw_mask.pieslice((0, 0, tl * 2, tl * 2), 180, 270, fill=0)
                if tr > 0:  # Top-right
                    draw_mask.pieslice((self.width - tr * 2, 0, self.width, tr * 2), 270, 0, fill=0)
                if br > 0:  # Bottom-right
                    draw_mask.pieslice((self.width - br * 2, self.height - br * 2, self.width, self.height), 0, 90, fill=0)
                if bl > 0:  # Bottom-left
                    draw_mask.pieslice((0, self.height - bl * 2, bl * 2, self.height), 90, 180, fill=0)
            
            # Only create and composite background if it's not fully transparent
            if self.alpha_background > 0:
                # Create background image with the specified color
                background = Image.new("RGBA", size, rgba_background)
                # Apply the mask to the background
                image = Image.composite(background, image, mask)
            else:
                # For transparent background, just use the mask directly to create a transparent shape
                image.putalpha(mask)

        else:
            # No rounded corners, just fill with background color if not transparent
            if self.alpha_background > 0:
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

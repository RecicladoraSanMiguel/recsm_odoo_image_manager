from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime

import os


class ImageModel:

    def __init__(self):
        self._font = font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '../assets/fonts/')+"Ubuntu-R.ttf", 18)
        self._topLeftHeightDivider = 10  # increase to make the textbox shorter in height
        self._topLeftWidthDivider = 5  # increase to make the textbox shorter in width
        self._textPadding = 2
        # Defines images size
        self._image_width = 400
        self._image_height = 300

    def _convert_image_to_thumbnail(self, img):
        img.thumbnail((self._image_width, self._image_height), Image.ANTIALIAS)

    def _add_image_timestamp(self, img, is_merged=False):
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))

        o = ImageDraw.Draw(overlay)

        o.rectangle(
            [0, 270, img.size[0], img.size[1]],
            fill=(0, 0, 0, 220)
        )

        o.text(
            [300 if is_merged else 120 + self._textPadding, 272 + self._textPadding],
            str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')),
            fill="white",
            font=self._font
        )
        return Image.alpha_composite(img, overlay)

    def merge_images(self, img1, img2):
        merged_image = Image.new("RGBA", (self._image_width * 2, self._image_height))

        merged_image.paste(img1)
        merged_image.paste(img2, (self._image_width, 0))

        return merged_image

    def process_image(self, img1, img2=False):
        self._convert_image_to_thumbnail(img1)
        image = ImageModel.get_rbga_image(img1)

        if img2:
            self._convert_image_to_thumbnail(img2)
            image = self.merge_images(img1, ImageModel.get_rbga_image(img2))

        image = self._add_image_timestamp(image, True if img2 else False)

        return image.tobytes()

    @staticmethod
    def get_rbga_image(img):
        return img.convert("RGBA")

    @staticmethod
    def convert_bytes_to_image(image_request_bytes):
        try:
            return Image.open(BytesIO(image_request_bytes))
        except IOError as e:
            print("== Unable to convert Bytes to Image ==")
            print(e)
            print("== End of Exception ==")
            return False


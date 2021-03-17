import base64
import random
import string
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw


class ImageCaptchaHelper:
    @staticmethod
    def generate_code():
        return ''.join(random.sample(string.ascii_letters + string.digits, 4))

    @staticmethod
    def generate_color():
        red = random.randint(50, 200)
        green = random.randint(50, 200)
        blue = random.randint(50, 200)
        return red, green, blue

    @staticmethod
    def generate_line(draw, width, height):
        for i in range(2):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(width / 2, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), 'black', 1)

    def generate_image_captcha(self):
        code = self.generate_code()
        width, height = 100, 50
        image = Image.new('RGB', (width, height), 'white')
        # font = ImageFont.truetype('DejaVuSans.ttf', 30)
        font = ImageFont.truetype('arial.ttf', 30)
        draw = ImageDraw.Draw(image)
        for i in range(4):
            draw.text((10 + random.randint(-10, 10) + 20 * i, 10 + random.randint(-10, 10)), code[i], self.generate_color(), font)
        self.generate_line(draw, width, height)
        return image, code

    def get_image_captcha(self):
        image, code = self.generate_image_captcha()
        buffer = BytesIO()
        image.save(buffer, 'jpeg')
        byte_code = buffer.getvalue()
        base64_code = base64.b64encode(byte_code)
        base64_str = base64_code.decode()
        return code, 'data:image/jpeg;base64,%s' % base64_str

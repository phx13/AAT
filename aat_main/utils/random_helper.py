import base64
import random
import string
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw


class RandomHelper:
    @staticmethod
    def generate_code(num):
        return ''.join(random.sample(string.ascii_letters + string.digits, num))

    @staticmethod
    def generate_color():
        red = random.randint(50, 200)
        green = random.randint(50, 200)
        blue = random.randint(50, 200)
        return red, green, blue

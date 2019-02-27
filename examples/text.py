#!/usr/bin/env python

import colorsys
import time
from sys import exit

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

import unicornhathd


print("""Unicorn HAT HD: Text

This example shows how to draw, display and scroll text in a regular
TrueType font on Unicorn HAT HD.

It uses the Python Pillow/PIL image library, and all other drawing functions
are available. See: http://pillow.readthedocs.io/en/3.1.x/reference/

""")


lines = ["In the old #BILGETANK we'll keep you in the know",
         "In the old #BILGETANK we'll fix your techie woes",
         "And we'll make things",
         "And we'll break things",
         "'til we're altogether aching",
         "Then we'll grab a cup of grog down in the old #BILGETANK"]

colours = [tuple([int(n * 255) for n in colorsys.hsv_to_rgb(x / float(len(lines)), 1.0, 1.0)]) for x in range(len(lines))]


# Use `fc-list` to show a list of installed fonts on your system,
# or `ls /usr/share/fonts/` and explore.

FONT = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 12)

# sudo apt install fonts-droid
# FONT = ('/usr/share/fonts/truetype/droid/DroidSans.ttf', 12)

# sudo apt install fonts-roboto
# FONT = ('/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf', 10)

unicornhathd.rotation(270)
unicornhathd.brightness(0.6)


width, height = unicornhathd.get_shape()

text_x = width
text_y = 2


font_file, font_size = FONT

font = ImageFont.truetype(font_file, font_size)

text_width, text_height = width, 0

try:
    for line in lines:
        w, h = font.getsize(line)
        text_width += w + width
        text_height = max(text_height, h)

    text_width += width + text_x + 1

    image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    offset_left = 0

    for index, line in enumerate(lines):
        draw.text((text_x + offset_left, text_y), line, colours[index], font=font)

        offset_left += font.getsize(line)[0] + width

    for scroll in range(text_width - width):
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x + scroll, y))
                r, g, b = [int(n) for n in pixel]
                unicornhathd.set_pixel(width - 1 - x, y, r, g, b)

        unicornhathd.show()
        time.sleep(0.01)

except KeyboardInterrupt:
    unicornhathd.off()

finally:
    unicornhathd.off()

#!/usr/bin/env python

import colorsys
import signal
import time
from sys import exit

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")

import unicornhathd


print("""Unicorn HAT HD: Text

This example shows how to draw, display and scroll text in a regular TrueType font on Unicorn HAT HD.

It uses the Python Pillow/PIL image library, and all other drawing functions are available.

See: http://pillow.readthedocs.io/en/3.1.x/reference/

""")

TEXT = "Hello World! How are you today? This is a real font!"

FONT = ("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 12)

# Use `fc-list` to show a list of installed fonts on your system,
# or `ls /usr/share/fonts/` and explore.

# sudo apt install fonts-droid
#FONT = ("/usr/share/fonts/truetype/droid/DroidSans.ttf", 12)

# sudo apt install fonts-roboto
#FONT = ("/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf", 10)

unicornhathd.rotation(0)
unicornhathd.brightness(0.5)

text_x = 1
text_y = 2

width, height = unicornhathd.get_shape()


font_file, font_size = FONT

font = ImageFont.truetype(font_file, font_size)

text_width, text_height = font.getsize(TEXT)

text_width += width + text_x

image = Image.new("RGB", (text_width,max(16, text_height)), (0,0,0))
draw = ImageDraw.Draw(image)

draw.text((text_x, text_y), TEXT, fill=(255, 255, 255), font=font)

for scroll in range(text_width - width):
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x+scroll, y))

            br, bg, bb = [int(n * 255) for n in colorsys.hsv_to_rgb((x + scroll) / float(text_width), 1.0, 1.0)]
            r, g, b = [float(n / 255.0) for n in pixel]
            r = int(br * r)
            g = int(bg * g)
            b = int(bb * b)

            unicornhathd.set_pixel(width-1-x, y, r, g, b)

    unicornhathd.show()
    time.sleep(0.01)

unicornhathd.off()

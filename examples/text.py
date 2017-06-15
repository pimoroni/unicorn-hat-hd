#!/usr/bin/env python

'''Unicorn HAT HD: Show a PNG image!

This basic example shows use of the Python Pillow library:

sudo pip-3.2 install pillow # or sudo pip install pillow

The tiny 16x16 bosses in lofi.png are from Oddball: http://forums.tigsource.com/index.php?topic=8834.0

Licensed under Creative Commons Attribution-Noncommercial-Share Alike 3.0 Unported License.

Press Ctrl+C to exit!

'''

import signal
import time
from sys import exit

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")

import unicornhathd as unicorn

print("""Unicorn HAT HD: Text

This example shows how to draw, display and scroll text in a regular TrueType font on Unicorn HAT HD.

It uses the Python Pillow/PIL image library, and all other drawing functions are available.

See: http://pillow.readthedocs.io/en/3.1.x/reference/

""")


FONT = ("/usr/share/fonts/truetype/droid/DroidSans.ttf", 12)
FONT = ("/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 10)

unicorn.rotation(0)
unicorn.brightness(0.5)

width, height = unicorn.get_shape()

text_width = 1000

font_file, font_size = FONT

image = Image.new("RGB", (text_width,16), (0,0,0))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(font_file, font_size)

draw.text((1, 2), "Hello World! How are you today? This is a real font!", fill=(255, 255, 255), font=font)

for scroll in range(text_width - width):
    c = 0

    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x+scroll, y))
            #print(pixel)
            r, g, b = [int(n) for n in pixel]
            unicorn.set_pixel(width-1-x, y, r, g, b)
            c += (r + g + b)

    unicorn.show()
    time.sleep(0.01)

    if c == 0: break


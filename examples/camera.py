#!/usr/bin/env python

# Inspired by Ben Nuttall's Astro Cam example,
# from: https://github.com/bennuttall/sense-hat-examples/blob/master/python/astro_cam.py
# Written by Dave Jones: https://gist.github.com/waveform80/a2621da13b88c3d751e31a15e97695c2
# Tweaked for Unicorn HAT HD

from signal import pause
from sys import exit

try:
    from picamera import PiCamera
except ImportError:
    exit('This script requires the picamera module\nInstall with: sudo pip install picamera')

try:
    from PIL import Image
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

import unicornhathd


print("""Unicorn HAT HD: Raspberry Pi Camera Display

Show a 16x16 feed from your Raspberry Pi camera!

Press Ctrl+C to exit.

""")


class DisplayOutput():
    def __init__(self):
        self.hat = unicornhathd
        self.hat.rotation(90)
        self.hat.brightness(0.6)

    def write(self, buf):
        img = Image.frombytes('RGB', (64, 64), buf)
        img = img.resize((16, 16), Image.BILINEAR)

        for x in range(16):
            for y in range(16):
                r, g, b = img.getpixel((x, y))
                self.hat.set_pixel(x, y, r, g, b)

        self.hat.show()


with PiCamera() as camera:
    camera.resolution = (64, 64)
    camera.contrast = 50
    camera.start_preview()
    output = DisplayOutput()
    camera.start_recording(output, 'rgb')

    try:
        pause()
    finally:
        camera.stop_recording()
        unicornhathd.off()

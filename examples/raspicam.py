#!/usr/bin/env python

# This is a modified version of Ben Nuttall's Astro Cam example,
# from: https://github.com/bennuttall/sense-hat-examples/blob/master/python/astro_cam.py

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    exit('This script requires the picamera module\nInstall with: sudo pip install picamera')

import unicornhathd


print("""Unicorn HAT HD: Raspberry Pi Camera Display

Show a 16x16 feed from your Raspberry Pi camera!

""")

while True:
    with PiCamera() as camera:
        camera.resolution = (32, 32)
        with PiRGBArray(camera, size=(16, 16)) as stream:
            camera.capture(stream, format='rgb', resize=(16, 16))
            image = stream.array

    for y, row in enumerate(image):
        for x, pixel in enumerate(row):
            r, g, b = pixel
            unicornhathd.set_pixel(x, y, r, g, b)

    unicornhathd.show()

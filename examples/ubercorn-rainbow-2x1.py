#!/usr/bin/env python

import colorsys
import math
import time

import unicornhathd


print("""Ubercorn rainbow 2x1

An example of how to use a 2-wide by 1-tall pair of Ubercorn matrices.

Press Ctrl+C to exit!

""")

unicornhathd.brightness(0.6)

# Enable addressing for Ubercorn matrices
unicornhathd.enable_addressing()

# Set up buffer shape to be 32 wide and 16 tall
unicornhathd.setup_buffer(32, 16)

# Set up display 0 on left, and display 1 on right
unicornhathd.setup_display(0, 0, 0, 0)
unicornhathd.setup_display(1, 16, 0, 0)

step = 0

try:
    while True:
        step += 1
        for x in range(0, 32):
            for y in range(0, 16):
                dx = 7
                dy = 7

                dx = (math.sin(step / 20.0) * 15.0) + 7.0
                dy = (math.cos(step / 15.0) * 15.0) + 7.0
                sc = (math.cos(step / 10.0) * 10.0) + 16.0

                h = math.sqrt(math.pow(x - dx, 2) + math.pow(y - dy, 2)) / sc

                r, g, b = colorsys.hsv_to_rgb(h, 1, 1)

                r *= 255.0
                g *= 255.0
                b *= 255.0

                unicornhathd.set_pixel(x, y, r, g, b)

        unicornhathd.show()
        time.sleep(1.0 / 60)

except KeyboardInterrupt:
    unicornhathd.off()

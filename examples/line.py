#!/usr/bin/env python

import time
import unicornhathd

print("""Unicorn HAT HD: Lines

Demonstrates how to draw lines on Unicorn HAT HD.

Press Ctrl+C to exit!
""")

unicornhathd.brightness(0.6)

try:
    while True:
        for rotation in [0, 90, 180, 270]:
            print('Showing lines at rotation: {}'.format(rotation))

            unicornhathd.clear()
            unicornhathd.rotation(rotation)
            unicornhathd.set_pixel(0, 0, 64, 64, 64)
            unicornhathd.show()
            time.sleep(0.5)

            for x in range(1, 16):
                unicornhathd.set_pixel(x, 0, 255, 0, 0)
                unicornhathd.show()
                time.sleep(0.5 / 16)

            time.sleep(0.5)

            for y in range(1, 16):
                unicornhathd.set_pixel(0, y, 0, 0, 255)
                unicornhathd.show()
                time.sleep(0.5 / 16)

            time.sleep(0.5)

            for b in range(1, 16):
                unicornhathd.set_pixel(b, b, 0, 255, 0)
                unicornhathd.show()
                time.sleep(0.5 / 16)

            time.sleep(0.5)

except KeyboardInterrupt:
    unicornhathd.off()

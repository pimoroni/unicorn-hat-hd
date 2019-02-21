#!/usr/bin/env python

import math
import time

# import random                    # Required for random values
# from colorsys import hsv_to_rgb  # required for trippy bar colours

import unicornhathd


print("""Unicorn HAT HD: Graph

This graph demo shows how you might display a range of values on UHHD.

Press Ctrl+C to exit!

""")

unicornhathd.rotation(90)
unicornhathd.brightness(0.6)
u_width, u_height = unicornhathd.get_shape()

bar_speed = 16
bar_width = 2
bar_colour = [64, 0, 128]

# Create our array of values to display on the chart
# These should always be scaled to the range 0.0 to 1.0

# Sine wave!
values = [(math.sin((x / 16.0) * math.pi) + 1.0) / 2.0 for x in range(32)]

# Random values
# values = [random.randint(0,127) / 127.0 for _ in range(32)]

try:
    while True:
        for x in range(u_width // bar_width):
            value = (values[x] * u_height)   # Scale the graph range 0.0 to 1.0 to the display height
            # Trippy bar colours!
            # bar_colour = [int(c * 255) for c in hsv_to_rgb(values[x] / 2, 1.0, 1.0)]
            for y in range(u_height):
                brightness = min(1.0, value - y)
                r, g, b = [int(c * brightness) for c in bar_colour]
                for z in range(bar_width):
                    unicornhathd.set_pixel((x * bar_width) + z, y, r, g, b)

        unicornhathd.show()
        values.append(values.pop(0))         # Move the first value to the end of the array
        time.sleep(1.0 / bar_speed)

except KeyboardInterrupt:
    unicornhathd.off()

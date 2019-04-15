#!/usr/bin/env python

import unicornhathd
import time
import colorsys
import numpy
import itertools

print("""Unicorn HAT HD: Heart Beats

Displaying a beating heart...

Your Unicorn HAT HD loves you.

<3

Press Ctrl+C to exit!

""")

unicornhathd.brightness(1)

# We rotate the heart to be the same orientation as the text on the rear
# of the Unicorn Hat HD
unicornhathd.rotation(270)

heart = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
         [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
         [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

heart = numpy.array(heart)

# Define the brightness levels for the heartbeat (lower numbers are dimmer)
# We let the minimum brightness be 1 so that there is still a visible heart
rising = range(1, 10, 1)    # [1...9]
ba = range(10, 5, -1)       # [10...6]
dum = range(5, 10, 1)       # [5...9]
falling = range(10, 0, -1)  # [10...1]

# Join the ranges together
pattern = (rising, ba, dum, falling)
brightness_levels = list(itertools.chain.from_iterable(pattern))

try:
    while True:
        # Go through each brightness level in the pattern
        for level in brightness_levels:
            for x in range(16):
                for y in range(16):
                    h = 0.0  # red
                    s = 1.0  # saturation at the top of the red scale
                    v = heart[x, y] * float(level) / 10     # brightness depends on range
                    r, g, b = colorsys.hsv_to_rgb(h, s, v)  # convert hsv back to RGB
                    red = int(r * 255.0)                    # makes 0-1 range > 0-255 range
                    green = int(g * 255.0)
                    blue = int(b * 255.0)
                    unicornhathd.set_pixel(x, y, red, green, blue)  # sets pixels on the hat
            unicornhathd.show()                             # show the pixels
            time.sleep(0.005)                               # tiny gap, sets frames to a smooth 200/sec
        time.sleep(0.8)                                     # waiting time between heartbeats

except KeyboardInterrupt:
    unicornhathd.off()

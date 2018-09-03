#!/usr/bin/env python

import colorsys
import math
from random import randint

import unicornhathd


print("""Unicorn HAT HD: Candle

This example simulates a flickering candle flame.

Press Ctrl+C to exit!

""")

unicornhathd.rotation(0)
width, height = unicornhathd.get_shape()
# buffer to contain candle "heat" data
candle = [0] * 256

# create a palette for mapping heat values onto colours
palette = [0] * 256
for i in range(0, 256):
    h = i / 5.0
    h /= 360.0
    s = (1.0 / (math.sqrt(i / 50.0) + 0.01))
    s = min(1.0, s)
    s = max(0.0, s)

    v = i / 200.0
    if i < 60:
        v = v / 2
    v = min(1.0, v)
    v = max(0.0, v)

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    palette[i] = (int(r * 255.0), int(g * 255.0), int(b * 255.0))


def set_pixel(b, x, y, v):
    b[y * 16 + x] = int(v)


def get_pixel(b, x, y):
    # out of range sample lookup
    if x < 0 or y < 0 or x >= 16 or y >= 16:
        return 0

    # subpixel sample lookup
    if isinstance(x, float) and x < 15:
        f = x - int(x)
        return (b[int(y) * 16 + int(x)] * (1.0 - f)) + (b[int(y) * 16 + int(x) + 1] * (f))

    # fixed pixel sample lookup
    return b[int(y) * 16 + int(x)]


step = 0

try:
    while True:
        # step for waving animation, adds some randomness
        step += randint(0, 15)

        # clone the current candle
        temp = candle[:]

        # seed new heat
        v = 500

        set_pixel(candle, 6, 15, v)
        set_pixel(candle, 7, 15, v)
        set_pixel(candle, 8, 15, v)
        set_pixel(candle, 9, 15, v)
        set_pixel(candle, 6, 14, v)
        set_pixel(candle, 7, 14, v)
        set_pixel(candle, 8, 14, v)
        set_pixel(candle, 9, 14, v)

        # blur, wave, and shift up one step
        for x in range(0, 16):
            for y in range(0, 16):
                s = math.sin((y / 30.0) + (step / 10.0)) * ((16 - y) / 20.0)
                v = 0
                for i in range(0, 3):
                    for j in range(0, 3):
                        # r = randint(0, 2) - 1
                        v += get_pixel(candle, x + i + s - 1, y + j)

                v /= 10
                set_pixel(temp, x, y, v)

        candle = temp

        # copy candle into UHHD with palette
        for x in range(0, 16):
            for y in range(0, 16):
                o = (i * 3) + 1
                r, g, b = palette[max(0, min(255, get_pixel(candle, x, y)))]
                unicornhathd.set_pixel(x, y, r, g, b)

        unicornhathd.show()

except KeyboardInterrupt:
    unicornhathd.off()

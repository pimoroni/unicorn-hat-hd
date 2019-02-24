#!/usr/bin/env python

#
# Ported from Pimoroni Unicorn HAT example
# https://github.com/pimoroni/unicorn-hat/blob/master/examples/hat/matrix.py
# to Unicorn HAT HD by aburgess@gmail.com (https://github.com/Mutiny-Games)

import time
from random import randint

import unicornhathd

print("""Unicorn HAT HD: Matrix HD

Follow the white rabbit...

Press Ctrl+C to exit!

""")

unicornhathd.rotation(90)
unicornhathd.brightness(0.6)

wrd_rgb = [
    [154, 173, 154], [0, 255, 0], [0, 235, 0], [0, 220, 0],
    [0, 185, 0], [0, 165, 0], [0, 128, 0], [0, 0, 0],
    [154, 173, 154], [0, 145, 0], [0, 125, 0], [0, 100, 0],
    [0, 80, 0], [0, 60, 0], [0, 40, 0], [0, 0, 0]
]

clock = 0

blue_pilled_population = [[randint(0, 15), 15]]

try:
    while True:
        for person in blue_pilled_population:
            y = person[1]
            for rgb in wrd_rgb:
                if (y <= 15) and (y >= 0):
                    unicornhathd.set_pixel(person[0], y, rgb[0], rgb[1], rgb[2])
                y += 1
            person[1] -= 1
        unicornhathd.show()
        time.sleep(0.1)
        clock += 1

        if clock % 5 == 0:
            blue_pilled_population.append([randint(0, 15), 15])
        if clock % 7 == 0:
            blue_pilled_population.append([randint(0, 15), 15])

        while len(blue_pilled_population) > 100:
            blue_pilled_population.pop(0)

except KeyboardInterrupt:
    unicornhathd.off()

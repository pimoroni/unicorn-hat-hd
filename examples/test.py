#!/usr/bin/env python

import time

import unicornhathd

print("""Unicorn HAT HD: Test

This example test the refresh rate of Unicorn HAT HD,
by rotating a random assortment of pixels one degree
at a time.

Press Ctrl+C to exit!

""")

unicornhathd.brightness(0.6)

unicornhathd.clear()
unicornhathd.set_all(10, 0, 10)
unicornhathd._buf = unicornhathd.numpy.random.randint(low=0,high=255,size=(16,16,3))

frame = 0
t_start = time.time()

try:
    while True:
        unicornhathd.show()
        unicornhathd.rotation(frame)
        frame += 1

except KeyboardInterrupt:
    print("FPS: {}".format(frame / (time.time() - t_start)))
    unicornhathd.off()

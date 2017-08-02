#!/usr/bin/env python

import time

import unicornhathd


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

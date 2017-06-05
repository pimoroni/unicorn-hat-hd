import time

import uhhd

uhhd.clear()
uhhd.set_all(10, 0, 10)

uhhd._buf = uhhd.numpy.random.randint(low=0,high=255,size=(16,16,3))

frame = 0
t_start = time.time()

try:
    while True:
        uhhd.show()
        uhhd.rotation(frame)
        frame += 1

except KeyboardInterrupt:
    print("FPS: {}".format(frame / (time.time() - t_start)))
    uhhd.clear()

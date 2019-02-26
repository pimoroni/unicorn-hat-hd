import unicornhathd as unicorn
import time
import colorsys
import numpy

unicorn.brightness(1)
# need to rotate the image to have the heart the right way up
unicorn.rotation(90)

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

while True:
    #  go through the range 1-10 backwards, then back up
    #  the 2* makes a ba-BUMP for the heart
    for i in 2 * (range(10,0,-1) + range(1, 10)):
        for y in range(16):
            for x in range(16):
                h = 0.0  # red
                s = 1.0  # saturation at the top of the red scale
                v = heart[x, y] / float(i)  # brightness depends on range
                rgb = colorsys.hsv_to_rgb(h, s, v)  # convert hsv back to RGB
                r = int(rgb[0]*255.0)  # makes 0-1 range > 0-255 range
                g = int(rgb[1]*255.0)
                b = int(rgb[2]*255.0)
                unicorn.set_pixel(x, y, r, g, b)  # sets pixels on the hat
        unicorn.show()  # show the pixels
        time.sleep(0.005)  # tiny gap, sets frames to a smooth 200/sec
    time.sleep(0.8)  # waiting time between heartbeats

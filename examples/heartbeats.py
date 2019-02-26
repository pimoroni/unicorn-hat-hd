import unicornhathd
import time
import colorsys
import numpy

print ("""Unicorn HAT HD: Heart Beats

Displaying a beating heart...

Your Unicorn HAT HD loves you.

<3

Press Ctrl+C to exit!

""")

unicornhathd.brightness(1)
# need to rotate the image to have the heart the right way up
unicornhathd.rotation(90)

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
                r, g, b = colorsys.hsv_to_rgb(h, s, v)  # convert hsv back to RGB
                red = int(r*255.0)  # makes 0-1 range > 0-255 range
                green = int(g*255.0)
                blue = int(b*255.0)
                unicornhathd.set_pixel(x, y, red, green, blue)  # sets pixels on the hat
        unicornhathd.show()  # show the pixels
        time.sleep(0.005)  # tiny gap, sets frames to a smooth 200/sec
    time.sleep(0.8)  # waiting time between heartbeats

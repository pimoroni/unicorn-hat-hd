import unicornhathhd as unicorn
import time, colorsys
import numpy

unicorn.brightness(1)
#need to rotate the image to have the heart the right way up
unicorn.rotation(90)

heart = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
         [0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0],
         [0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0],
         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
         [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
         [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
         [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
         [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
         [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
         [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]  

heart = numpy.array(heart)

while True:
# go through the range 1-10 backwards then back up
# the 2* makes a ba-BUMP for the heart
  for i in 2*(range(1,11)[::-1]+range(1,10)):
# the x and y ranges are the size of the Unicorn Hat HD - 16 x 16 pixels
    for y in range(16):
      for x in range(16):
        h = 0.0 # red
        s = 1.0 # saturation at the top of the red scale
        v = heart[x,y] / float(i) # the brightness of the heart depeds where it is in the range
        rgb = colorsys.hsv_to_rgb(h, s, v) # convert the hsv back to RGB
        r = int(rgb[0]*255.0) # makes a 0-1 range into a 0-255 range and rounds it to a whole number
        g = int(rgb[1]*255.0)
        b = int(rgb[2]*255.0)
        unicorn.set_pixel(x, y, r, g, b) # sets the pixels on the unicorn hat
    unicorn.show() # show the pixels
    time.sleep(0.005) # tiny gap, sets the frames of the heart animation to 200 a second so it looks smooth
  time.sleep(0.8) # waiting time between heartbeats

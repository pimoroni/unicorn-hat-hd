#!/usr/bin/env python

import colorsys
import time

try:
    import spidev
except ImportError:
    sys.exit("This library requires the spidev module\nInstall with: sudo pip install spidev")

try:
    import numpy
except ImportError:
    exit("This library requires the numpy module\nInstall with: sudo pip install numpy")


__version__ = '0.0.2'

_spi = spidev.SpiDev()
_spi.open(0, 0)
_spi.max_speed_hz = 9000000
_SOF = 0x72
_DELAY = 1.0/120

WIDTH = 16
HEIGHT = 16

PHAT = None
HAT = None
PHAT_VERTICAL = None
AUTO = None

_rotation = 90
_brightness = 0.5
_buf = numpy.zeros((16,16,3), dtype=int)

def brightness(b):
    """Set the display brightness between 0.0 and 1.0.

    :param b: Brightness from 0.0 to 1.0 (default 0.2)

    """

    global _brightness

    _brightness = b

def rotation(r):
    """Set the display rotation in degrees.

    Actual rotation will be snapped to the nearest 90 degrees.

    """
    global _rotation

    _rotation = int(round(r/90.0))

def get_rotation():
    """Returns the display rotation in degrees."""
    return _rotation * 90

def set_layout(pixel_map=None):
    """Does nothing, for library compatibility with Unicorn HAT."""
    pass

def set_all(r, g, b):
    _buf[:] = r, g, b    

def set_pixel(x, y, r, g, b):
    """Set a single pixel to RGB colour.

    :param x: Horizontal position from 0 to 7
    :param y: Veritcal position from 0 to 7
    :param r: Amount of red from 0 to 255
    :param g: Amount of green from 0 to 255
    :param b: Amount of blue from 0 to 255

    """
    _buf[x][y] = r, g, b

def set_pixel_hsv(x, y, h, s=1.0, v=1.0):
    """set a single pixel to a colour using HSV.

     :param x: Horizontal position from 0 to 7
     :param y: Veritcal position from 0 to 7
     :param h: Hue from 0.0 to 1.0 ( IE: degrees around hue wheel/360.0 )
     :param s: Saturation from 0.0 to 1.0
     :param v: Value (also known as brightness) from 0.0 to 1.0

    """

    r, g, b = [int(n*255) for n in colorsys.hsv_to_rgb(h, s, v)]
    set_pixel(x, y, r, g, b)

def get_pixel(x, y):
    return tuple(_buf[x][y])

def shade_pixels(shader):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            r, g, b = shader(x, y)
            set_pixel(x, y, r, g, b)

def get_pixels():
    return _buf

def get_shape():
    """Return the shape (width, height) of the display."""

    return WIDTH, HEIGHT

def clear():
    """Clear the buffer."""
    _buf.fill(0)

def off():
    """Clear the buffer and immediately update Unicorn HAT HD.

    Turns off all pixels.

    """
    clear()
    show()

def show():
    """Output the contents of the buffer to Unicorn HAT HD."""
    _spi.xfer2([_SOF] + (numpy.rot90(_buf,_rotation).reshape(768) * _brightness).astype(numpy.uint8).tolist())
    time.sleep(_DELAY)


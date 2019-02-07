#!/usr/bin/env python
"""Unicorn HAT HD library.

Drive the 16x16 RGB pixel Pimoronu Unicorn HAT HD
over SPI from a Raspberry Pi or compatible platform.

"""

import colorsys
import time


try:
    import spidev
except ImportError:
    raise ImportError('This library requires the spidev module\nInstall with: sudo pip install spidev')

try:
    import numpy
except ImportError:
    raise ImportError('This library requires the numpy module\nInstall with: sudo pip install numpy')


__version__ = '0.0.4'

_SOF = 0x72
_DELAY = 1.0 / 120

WIDTH = 16
HEIGHT = 16

PHAT = None
HAT = None
PHAT_VERTICAL = None
AUTO = None
PANEL_SHAPE = (16, 16)


_rotation = 0
_brightness = 0.5
_buffer_width = 16
_buffer_height = 16
_addressing_enabled = False
_buf = numpy.zeros((_buffer_width, _buffer_height, 3), dtype=int)


class Display:
    """Represents a single display in a multi-display chain.

    Contains the coordinates for the slice of the pixel buffer
    which should be visible on this particular display.

    """

    def __init__(self, enabled, x, y, rotation):
        """Initialise display.

        :param enabled: True/False to indicate if this display is enabled
        :param x: x offset of display portion in buffer
        :param y: y offset of display portion in buffer
        :param rotation: rotation of display

        """
        self.enabled = enabled
        self.update(x, y, rotation)

    def update(self, x, y, rotation):
        """Update display position.

        :param x: x offset of display portion in buffer
        :param y: y offset of display portion in buffer
        :param rotation: rotation of display

        """
        self.x = x
        self.y = y
        self.rotation = rotation

    def get_buffer_window(self, source):
        """Grab the correct portion of the supplied buffer for this display.

        :param source: source buffer, should be a numpy array

        """
        view = source[self.x:self.x + PANEL_SHAPE[0], self.y:self.y + PANEL_SHAPE[1]]
        return numpy.rot90(view, self.rotation + 1)


_displays = [Display(False, 0, 0, 0) for _ in range(8)]

is_setup = False


def setup():
    """Initialize Unicorn HAT HD."""
    global _spi, _buf, is_setup

    if is_setup:
        return

    _spi = spidev.SpiDev()
    _spi.open(0, 0)
    _spi.max_speed_hz = 9000000

    is_setup = True


def enable_addressing(enabled=True):
    """Enable multi-panel addressing support (for Ubercorn)."""
    global _addressing_enabled
    _addressing_enabled = enabled


def setup_buffer(width, height):
    """Set up the internal pixel buffer.

    :param width: width of buffer, ideally in multiples of 16
    :param height: height of buffer, ideally in multiples of 16

    """
    global _buffer_width, _buffer_height, _buf

    _buffer_width = width
    _buffer_height = height
    _buf = numpy.zeros((_buffer_width, _buffer_height, 3), dtype=int)


def enable_display(address, enabled=True):
    """Enable a single display in the chain.

    :param address: address of the display from 0 to 7
    :param enabled: True/False to indicate display is enabled

    """
    _displays[address].enabled = enabled


def setup_display(address, x, y, rotation):
    """Configure a single display in the chain.

    :param x: x offset of display portion in buffer
    :param y: y offset of display portion in buffer
    :param rotation: rotation of display

    """
    _displays[address].update(x, y, rotation)
    enable_display(address)


def brightness(b):
    """Set the display brightness between 0.0 and 1.0.

    :param b: Brightness from 0.0 to 1.0 (default 0.5)

    """
    global _brightness

    _brightness = b


def rotation(r):
    """Set the display rotation in degrees.

    Actual rotation will be snapped to the nearest 90 degrees.

    """
    global _rotation

    _rotation = int(round(r / 90.0))


def get_rotation():
    """Return the display rotation in degrees."""
    return _rotation * 90


def set_layout(pixel_map=None):
    """Do nothing, for library compatibility with Unicorn HAT."""
    pass


def set_all(r, g, b):
    """Set all pixels to RGB colour.

    :param r: Amount of red from 0 to 255
    :param g: Amount of green from 0 to 255
    :param b: Amount of blue from 0 to 255

    """
    _buf[:] = r, g, b


def set_pixel(x, y, r, g, b):
    """Set a single pixel to RGB colour.

    :param x: Horizontal position from 0 to 15
    :param y: Veritcal position from 0 to 15
    :param r: Amount of red from 0 to 255
    :param g: Amount of green from 0 to 255
    :param b: Amount of blue from 0 to 255

    """
    _buf[int(x)][int(y)] = r, g, b


def set_pixel_hsv(x, y, h, s=1.0, v=1.0):
    """Set a single pixel to a colour using HSV.

    :param x: Horizontal position from 0 to 15
    :param y: Veritcal position from 0 to 15
    :param h: Hue from 0.0 to 1.0 ( IE: degrees around hue wheel/360.0 )
    :param s: Saturation from 0.0 to 1.0
    :param v: Value (also known as brightness) from 0.0 to 1.0

    """
    r, g, b = [int(n * 255) for n in colorsys.hsv_to_rgb(h, s, v)]
    set_pixel(x, y, r, g, b)


def get_pixel(x, y):
    """Get pixel colour in RGB as a tuple.

    :param x: Horizontal position from 0 to 15
    :param y: Veritcal position from 0 to 15

    """
    return tuple(_buf[int(x)][int(y)])


def shade_pixels(shader):
    """Set all pixels to a colour determined by a shader function.

    :param shader: function that accepts x/y position and returns an r,g,b tuple.

    """
    for x in range(WIDTH):
        for y in range(HEIGHT):
            r, g, b = shader(x, y)
            set_pixel(x, y, r, g, b)


def get_pixels():
    """Return entire buffer."""
    return _buf


def get_shape():
    """Return the shape (width, height) of the display."""
    return _buffer_width, _buffer_height


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
    setup()
    if _addressing_enabled:
        for address in range(8):
            display = _displays[address]
            if display.enabled:
                if _buffer_width == _buffer_height or _rotation in [0, 2]:
                    window = display.get_buffer_window(numpy.rot90(_buf, _rotation))
                else:
                    window = display.get_buffer_window(numpy.rot90(_buf, _rotation))

                _spi.xfer2([_SOF + 1 + address] + (window.reshape(768) * _brightness).astype(numpy.uint8).tolist())
                time.sleep(_DELAY)
    else:
        _spi.xfer2([_SOF] + (numpy.rot90(_buf, _rotation).reshape(768) * _brightness).astype(numpy.uint8).tolist())

    time.sleep(_DELAY)

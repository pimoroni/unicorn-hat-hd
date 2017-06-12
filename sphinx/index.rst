.. role:: python(code)
   :language: python

Welcome
-------

This documentation will guide you through the methods available in the Unicorn HAT HD python library.

Unicorn HAT HD provides a matrix of 256 RGB pixels that is ideal for writing messages, showing graphs, and drawing pictures. Use it to output your IP address, show CPU usage, or just play pong!

* More information - https://shop.pimoroni.com/products/unicorn-hat-hd
* Get the code - https://github.com/pimoroni/unicorn-hat-hd
* GPIO pinout - https://pinout.xyz/pinout/unicorn_hat_hd
* Get help - http://forums.pimoroni.com/c/support

At A Glance
-----------

.. automoduleoutline:: unicornhathd
   :members:

.. toctree::
   :titlesonly:
   :maxdepth: 0

Set A Pixel
-----------

.. automodule:: unicornhathd
   :noindex:
   :members: set_pixel, set_pixel_hsv

Set Brightness
--------------

.. automodule:: unicornhathd 
   :noindex:
   :members: brightness

Set Rotation
------------

.. automodule:: unicornhathd
   :noindex:
   :members: rotation, get_rotation

Show The Buffer
---------------

.. automodule:: unicornhathd
   :noindex:
   :members: show

Clear The Buffer
----------------

.. automodule:: unicornhathd
   :noindex:
   :members: clear

Clear The Display
-----------------

.. automodule:: unicornhathd
   :noindex:
   :members: off

Porting From Unicorn HAT
------------------------

The Unicorn HAT HD library has been structured to make it easier to port your code from Unicorn HAT.

A couple of methods exist solely for this purpose; get_shape and set_layout:

.. automodule:: unicornhathd
   :noindex:
   :members: get_shape, set_layout

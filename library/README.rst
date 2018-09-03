|Unicorn HAT HD| http://shop.pimoroni.com/products/unicorn-hat-hd

|Build Status| |Coverage Status| |PyPi Package| |Python Versions|

Installing
----------

Full install (recommended):
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We've created an easy installation script that will install all
pre-requisites and get your Unicorn HAT HD up and running with minimal
efforts. To run it, fire up Terminal which you'll find in Menu ->
Accessories -> Terminal on your Raspberry Pi desktop, as illustrated
below:

.. figure:: http://get.pimoroni.com/resources/github-repo-terminal.png
   :alt: Finding the terminal

   Finding the terminal

In the new terminal window type the command exactly as it appears below
(check for typos) and follow the on-screen instructions:

.. code:: bash

    curl https://get.pimoroni.com/unicornhathd | bash

If you choose to download examples you'll find them in
``/home/pi/Pimoroni/unicornhathd/``. To prototype and try out your code
without having to deploy it onto a Raspberry Pi every time, you can use
the `Unicorn HAT
simulator <https://github.com/jayniz/unicorn-hat-sim>`__ to run a mock
Unicorn HAT on your computer.

Manual install:
~~~~~~~~~~~~~~~

SPI needs to be enabled to communicate with the Unicorn Hat HD. If the
SPI on your Pi is not enabled or you are unsure if it is:

.. code:: bash

    sudo raspi-config nonint do_spi 0
    sudo reboot

Library install for Python 3:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    sudo apt-get install python3-pip python3-dev python3-spidev
    sudo pip3 install unicornhathd

Library install for Python 2:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    sudo apt-get install python-pip python-dev python-spidev
    sudo pip install unicornhathd

Development:
~~~~~~~~~~~~

If you want to contribute, or like living on the edge of your seat by
having the latest code, you should clone this repository, ``cd`` to the
library directory, and run:

.. code:: bash

    sudo apt-get install python-dev python-setuptools
    sudo python3 setup.py install

(or ``sudo python setup.py install`` whichever your primary Python
environment may be)

In all cases you will have to enable the SPI bus.

Documentation & Support
-----------------------

-  Guides and tutorials - https://learn.pimoroni.com/unicorn-hat-hd
-  Function reference - http://docs.pimoroni.com/unicornhathd/
-  GPIO Pinout - http://pinout.xyz/pinout/unicorn\_hat\_hd
-  Get help - http://forums.pimoroni.com/c/support

.. |Unicorn HAT HD| image:: unicorn-hat-hd-logo.png
.. |Build Status| image:: https://travis-ci.com/pimoroni/unicorn-hat-hd.svg?branch=master
   :target: https://travis-ci.com/pimoroni/unicorn-hat-hd
.. |Coverage Status| image:: https://coveralls.io/repos/github/pimoroni/unicorn-hat-hd/badge.svg?branch=master
   :target: https://coveralls.io/github/pimoroni/unicorn-hat-hd?branch=master
.. |PyPi Package| image:: https://img.shields.io/pypi/v/unicornhathd.svg
   :target: https://pypi.python.org/pypi/unicornhathd
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/unicornhathd.svg
   :target: https://pypi.python.org/pypi/unicornhathd

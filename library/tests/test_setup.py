"""Test various import and setup routines."""
import sys
import mock
import pytest


def test_setup():
    """Test that the library sets up correctly with numpy and spidev."""
    sys.modules['spidev'] = mock.MagicMock()
    import unicornhathd
    unicornhathd.setup()


def test_brightness():
    """Test brightness API change and alias."""
    sys.modules['spidev'] = mock.MagicMock()
    import unicornhathd
    unicornhathd.setup()

    unicornhathd.set_brightness(0.5)
    assert unicornhathd.set_brightness == unicornhathd.brightness


def test_rotation():
    """Test rotation API change and alias."""
    sys.modules['spidev'] = mock.MagicMock()
    import unicornhathd
    unicornhathd.setup()

    unicornhathd.set_rotation(90)
    assert unicornhathd.set_rotation == unicornhathd.rotation


def test_tuple_colour():
    """Test valid text colour."""
    sys.modules['spidev'] = mock.MagicMock()
    import unicornhathd
    unicornhathd.setup()

    unicornhathd.set_pixel(0, 0, (255, 0, 0))

    assert tuple(unicornhathd._buf[0, 0]) == (255, 0, 0)


def test_valid_text_colour():
    """Test valid text colour."""
    sys.modules['spidev'] = mock.MagicMock()
    import unicornhathd
    unicornhathd.setup()

    unicornhathd.set_pixel(0, 0, 'Teal')

    assert tuple(unicornhathd._buf[0, 0]) == unicornhathd.COLORS['teal']


def test_invalid_text_colour():
    """Test valid text colour."""
    sys.modules['spidev'] = mock.MagicMock()
    import unicornhathd
    unicornhathd.setup()

    with pytest.raises(ValueError):
        unicornhathd.set_pixel(0, 0, 'Octarine')

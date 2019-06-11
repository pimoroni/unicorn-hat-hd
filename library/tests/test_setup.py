"""Test various import and setup routines."""
import sys
import mock


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

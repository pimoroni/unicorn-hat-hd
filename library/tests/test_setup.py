"""Test various import and setup routines."""
import sys
import mock


def test_setup():
    """Test that the library sets up correctly with numpy and spidev."""
    sys.modules['spidev'] = mock.MagicMock()
    import unicornhathd
    unicornhathd.setup()

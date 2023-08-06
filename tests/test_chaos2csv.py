"""Test module for chaos2csv."""

from chaos2csv import __author__, __email__, __version__


def test_project_info():
    """Test __author__ value."""
    assert __author__ == "MaKaNu"
    assert __email__ == "matti dot kaupenjohann at fh minus dortmund dot de"
    assert __version__ == "0.0.0"

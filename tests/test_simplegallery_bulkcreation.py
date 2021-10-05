import pytest

from simplegallery_bulkcreation import core


def test_read_config_empty():
    defaults, galleries = core.read_config("file_which_does_not_exists")
    assert defaults == {
        "gallery_root": ".",
        "title": "A Photo Gallery",
        "description": "This is a cool Photo gallery",
        "title_photo": "",
        "title_photo_offset": "",
    }
    assert galleries == []

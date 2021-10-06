import shutil
from pathlib import Path

from simplegallery_bulkcreation import core


def cleanup_after_tests():
    path = Path("example/gallery")
    shutil.rmtree(path)
    return True


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


def test_read_config():
    defaults, galleries = core.read_config("example/config-example.ini")
    assert defaults == {
        "gallery_root": "example/gallery",
        "title": "My vacations",
        "description": "The best days of the year",
        "title_photo": "example/pictures/mexico2017/2017-11-01_15-20-23.jpg",
        "title_photo_offset": "20",
    }
    assert galleries == [
        {
            "name": "Oman 2020",
            "pathname": "Oman_2020",
            "image_source": "example/pictures/oman2020",
            "description": "Some days in the orient",
            "background_photo": "2020-02-02_18-40-33.jpg",
            "background_photo_offset": 30,
            "overview_photo": "2020-02-02_18-40-33.jpg",
            "url": "",
        },
        {
            "name": "Greece 2019",
            "pathname": "Greece_2019",
            "image_source": "example/pictures/greece2019",
            "description": "Island hoping in Greece",
            "background_photo": "2019-08-29_10-19-43.jpg",
            "background_photo_offset": "40",
            "overview_photo": "2019-08-29_10-19-43.jpg",
            "url": "",
        },
    ]


def test_create_overview_public():
    data_path = "src/simplegallery_bulkcreation/data"

    defaults, galleries = core.read_config(config_path="example/config-example.ini")
    root_dir = defaults["gallery_root"]

    core.create_overview_public(root_dir, data_path, defaults, galleries)
    assert Path("example/gallery/public/index.html").exists()
    assert Path("example/gallery/public/css/main.css").exists()
    assert Path("example/gallery/public/css/default-skin.css").exists()
    assert (
        Path("example/gallery/public/css/main.css").read_text()
        == Path("src/simplegallery_bulkcreation/data/public/css/main.css").read_text()
    )
    assert (
        Path("example/gallery/public/css/default-skin.css").read_text()
        == Path(
            "src/simplegallery_bulkcreation/data/public/css/default-skin.css"
        ).read_text()
    )
    cleanup_after_tests()

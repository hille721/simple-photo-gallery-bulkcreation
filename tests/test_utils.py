from pathlib import Path
import platform
import shutil

from simplegallery_bulkcreation.utils import copytree, pltostr


def test_pltostr():
    if platform.system() != "Windows":
        assert (
            str(Path("/just/an/example").absolute())
            == pltostr(Path("/just/an/example"))
            == pltostr("/just/an/example")
            == "/just/an/example"
        )
    else:
        # on Windows the string is not "/just/an/example", but anything as D:\just\an\example
        # thus we simple skip that
        assert str(Path("/just/an/example").absolute()) == pltostr(
            Path("/just/an/example")
        )


def test_copytree():
    assert copytree(
        Path("src/simplegallery_bulkcreation/data/public"),
        Path("example/gallery/tmp"),
    )
    # let's run it again to check if it also run if the directory already exists
    assert copytree(
        Path("src/simplegallery_bulkcreation/data/public"),
        Path("example/gallery/tmp"),
    )
    shutil.rmtree(Path("example/gallery"))
    # doing the same with more parent paths
    assert copytree(
        Path("src/simplegallery_bulkcreation/data/public"),
        Path("example/gallery/tmp/tmp"),
    )
    shutil.rmtree(Path("example/gallery"))

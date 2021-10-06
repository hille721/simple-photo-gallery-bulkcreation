""" some general helping functions """
import sys

if sys.version_info.major < 3:
    sys.exit("Python 2 not supported!")
if sys.version_info.major == 3 and sys.version_info.minor < 8:
    from distutils.dir_util import copy_tree

    LEGACY_SUPPORT = True
else:
    import shutil

    LEGACY_SUPPORT = False


def copytree(src, dst):
    """
    Wrapper around `shutil.copytree` function to support also Python < 3.8 (see #3).

    Backround:
        The `shutil.copytree` option `dirs_exist_ok=True` was introduced in Python 3.8
        To support Python 3.6 and Python 3.7 as well, we have to do a workaround
        and using the `copy_tree` function of the `distutils.dir_util` module.

    Args:
        src (Path): source path
        dst (Path): destination path
    """
    if LEGACY_SUPPORT:
        return copy_tree(str(src.absolute()), str(dst.absolute()))

    return shutil.copytree(  # pylint: disable=unexpected-keyword-arg
        src, dst, dirs_exist_ok=True
    )

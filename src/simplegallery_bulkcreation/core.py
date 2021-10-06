#!/usr/bin/env python
"""main functions of the nestedphotogallery package"""

import argparse
import configparser
from pathlib import Path
import shutil
import sys

import jinja2
import pkg_resources

from simplegallery_bulkcreation.utils import copytree
from simplegallery_bulkcreation.galleryclass import SimpleGallery, spg_common

if sys.version_info.major < 3:
    sys.exit("Python 2 not supported!")


def parse_args():
    """
    Configures the argument parser
    """

    description = "Plugin for the simple-photo-gallery"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "config_file",
        help="Config file which should be used.",
    )

    return parser.parse_args()


def read_config(config_path="./config-example.ini"):
    """read config file"""

    config = configparser.ConfigParser()
    config.read(config_path)

    defaults = {}
    galleries = []
    for name, values in config.items():
        if name == "DEFAULT":
            defaults = dict(
                gallery_root=values.get("gallery_root", "."),
                title=values.get("title", "A Photo Gallery"),
                description=values.get("description", "This is a cool Photo gallery"),
                title_photo=values.get("title_photo", ""),
                title_photo_offset=values.get("title_photo_offset", ""),
            )
            continue

        galleries.append(
            dict(
                name=name,
                pathname=name.replace(" ", "_"),
                image_source=values.get("image_source", "."),
                description=values.get("description", ""),
                background_photo=values.get("background_photo", ""),
                background_photo_offset=values.get("background_photo_offset", 30),
                overview_photo=values.get(
                    "overview_photo", values.get("background_photo", "")
                ),
                url=values.get("url", ""),
            )
        )

    return defaults, galleries


def write_overview_index(public_dir, defaults, galleries, template_path):
    """render & write overview site index.html"""

    file_loader = jinja2.FileSystemLoader(template_path)
    env = jinja2.Environment(loader=file_loader)
    template = env.get_template("index_template.jinja")
    index_html = public_dir / "index.html"
    index_html.write_text(template.render(defaults=defaults, galleries=galleries))

    return True


def create_overview_public(root_dir, data_path, defaults, galleries):
    """
    Create index.html of overview gallery root site.

    Args:
        root_dir (str): path to the root site dictionary
        data_path (str): path to the package data directory
        defaults (dict): dictionary of the defaults
        galleries (list): list of dictionaries of the galleries
    """

    public_dir = Path(root_dir) / "public"
    data_dir = Path(data_path)
    title_photo = Path(defaults["title_photo"])

    spg_common.log(f"Creating overview index page under {public_dir}...")

    # move css into public directory
    copytree(data_dir / "public", public_dir)
    if title_photo.exists():
        shutil.copy(title_photo, public_dir / title_photo.name)
        defaults["title_photo"] = title_photo.name

    # generate root index.html
    write_overview_index(public_dir, defaults, galleries, data_dir / "templates")
    spg_common.log(f"Overview index page {public_dir}/index.html created successfully!")


def main():
    """
    main function of the package
    """

    # Parse the arguments
    args = parse_args()
    config_path = Path(args.config_file)

    if not config_path.is_file():
        sys.exit(f"Config file {config_path.absolute()} not found")
    data_path = Path(
        pkg_resources.resource_filename("simplegallery_bulkcreation", "data")
    )

    defaults, galleries = read_config(config_path=config_path)
    root_dir = defaults["gallery_root"]
    seperator_line = "----------------------------------------"

    spg_common.log(seperator_line)
    create_overview_public(root_dir, data_path, defaults, galleries)
    spg_common.log(seperator_line)

    for gallery_conf in galleries:
        # TODO: Exception handling!
        try:
            gallery = SimpleGallery(root_dir, **gallery_conf)
            gallery.gallery_init()
            spg_common.log(seperator_line)
            gallery.gallery_build()
            spg_common.log(seperator_line)
        except Exception as exc:
            sys.exit(str(exc))
    spg_common.log(f"All galleries were built successfully. Open {root_dir}/public.")

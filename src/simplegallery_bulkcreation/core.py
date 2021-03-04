#!/usr/bin/env python
'''main functions of the nestedphotogallery package'''

from pathlib import Path
import configparser
import shutil
import sys

import jinja2

from simplegallery_bulkcreation.galleryclass import SimpleGallery


def read_config(config_path='./config-example.ini'):
    ''' read config file '''

    config = configparser.ConfigParser()
    config.read(config_path)

    defaults = {}
    galleries = []
    for name, values in config.items():
        if name == 'DEFAULT':
            defaults = dict(
                gallery_root=values.get('gallery_root', '.'),
                title=values.get('title', 'A Photo Gallery'),
                description=values.get('description', 'This is a cool Photo gallery'),
                title_photo=values.get('title_photo',''),
                title_photo_offset=values.get('title_photo_offset','')
            )
            continue

        galleries.append(dict(
            name=name,
            pathname=name.replace(' ', '_'),
            image_source=values.get('image_source', '.'),
            description=values.get('description', ''),
            background_photo=values.get('background_photo', ''),
            background_photo_offset=values.get('background_photo_offset', 30),
            overview_photo=values.get('overview_photo', values.get('background_photo', '')),
            url=values.get('url', '')
        ))

    return defaults, galleries


def write_overview_index(public_dir, defaults, galleries, template_path):
    ''' render & write overview site index.html '''

    file_loader = jinja2.FileSystemLoader(template_path)
    env = jinja2.Environment(loader=file_loader)
    template = env.get_template("index_template.jinja")
    index_html = public_dir / 'index.html'
    index_html.write_text(template.render(defaults=defaults, galleries=galleries))

    return True


def create_overview_public(root_dir, data_path, defaults, galleries):

    public_dir = Path(root_dir) / 'public'
    data_dir = Path(data_path)
    title_photo = Path(defaults['title_photo'])

    ### move css into public directory
    shutil.copytree(data_dir / 'public', public_dir, dirs_exist_ok=True)
    if title_photo.exists():
        shutil.copy(title_photo, data_dir / 'public' / title_photo.name)
        defaults['title_photo'] = title_photo.name

    ### generate root index.html
    write_overview_index(public_dir, defaults, galleries, data_dir / 'templates')


def main():

    #TODO: Change this
    config_path = "config-example.ini"
    data_path = "src/simplegallery_bulkcreation/data/"

    defaults, galleries = read_config(config_path=config_path)
    root_dir = defaults['gallery_root']

    create_overview_public(root_dir, data_path, defaults, galleries)

    for gallery_conf in galleries:
        # TODO: Exception handling!
        try:
            gallery = SimpleGallery(root_dir, **gallery_conf)
            gallery.gallery_init()
            gallery.gallery_build()
        except Exception as exc:
            sys.exit(str(exc))

''' Handling one gallery folder '''

import json
from pathlib import Path
import shutil

import pkg_resources

import simplegallery.common as spg_common
from simplegallery import gallery_build
from simplegallery.logic.gallery_logic import get_gallery_logic


def _pltostr(path):
    '''
    convert Pathlib object to absolute path as string

    Args:
        path (Path object): Pathobject to convert
    '''
    if isinstance(path, str):
        return path
    return str(path.absolute())

class SimpleGallery:
    '''
    Object class for one gallery

    Args:
        root_dir (str): path to the root directory of the gallery overview
        name (str, optional): gallery name. Defaults to ''.
        pathname (str, optional): gallery pathname. Defaults to ''.
        image_source (str, optional): image source directory. Defaults to '.'.
        description (str, optional): description of the gallery. Defaults to ''.
        background_photo (str, optional): background picture of the gallery. Defaults to "".
        background_photo_offset (int, optional): background picture offset. Defaults to 30.
        url (str, optional): url of the gallery. Defaults to "".

    Raises:
        RuntimeError: will be raised for any error
    '''

    def __init__(self, root_dir, name='', pathname='', image_source='.', description='',
                 background_photo="", background_photo_offset=30,
                 url="", **kwargs):

        self.name = name
        self.pathname = pathname
        self.description = description
        self.gallery_path = Path(root_dir) / 'galleries_data' / pathname
        self.public_dir = Path(root_dir) / 'public'
        self.public_gallery_dir = self.public_dir / self.pathname
        self.image_source = Path(image_source)
        self.gallery_config_path = self.gallery_path / 'gallery.json'
        self.background_photo = background_photo
        self.background_photo_offset = background_photo_offset
        self.url = url

        if not self.gallery_path.exists():
            self.gallery_path.mkdir(parents=True)

        if not self.image_source.exists():
            ### TODO: Implement Error Handling
            raise RuntimeError(f'image source directory {image_source} does not exists')

    def _create_gallery_json(self):
        ''' Build the gallery config '''

        gallery_config = dict(
            images_data_file=_pltostr(self.gallery_path / 'images_data.json'),
            public_path=_pltostr(self.public_gallery_dir),
            templates_path=_pltostr(self.gallery_path / 'templates'),
            images_path=_pltostr(self.public_gallery_dir / 'images' / 'photos'),
            thumbnails_path=_pltostr(self.public_gallery_dir / 'images' / 'thumbnails'),
            thumbnail_height=160,
            title=self.name,
            description=self.description,
            background_photo=self.background_photo,
            background_photo_offset=self.background_photo_offset,
            url=self.url,
        )

        self.gallery_config_path.write_text(
            json.dumps(gallery_config, indent=4, separators=(",", ": "))
            )

        spg_common.log("Gallery config stored in gallery.json")

        return True

    def _create_folder_structure(self):
        '''
        Creates the gallery folder structure by copying all the gallery templates
        and moving all images and videos to the
        photos subfolder.
        We can't use `simplegallery.gallery-init.create_gallery_folder_structure`
        because there is no possibility to set
        another public folder
        '''
        # Copy the public and templates folder
        spg_common.log("Copying gallery template files...")
        shutil.copytree(
            Path(pkg_resources.resource_filename("simplegallery", "data/templates")),
            self.gallery_path / 'templates',
            dirs_exist_ok=True
        )
        shutil.copytree(
            Path(pkg_resources.resource_filename("simplegallery", "data/public")),
            self.public_gallery_dir,
            dirs_exist_ok=True
        )

        photos_dir = self.public_gallery_dir / 'images' / 'photos'
        if not photos_dir.exists():
            photos_dir.mkdir(parents=True)
        spg_common.log(f'Moving all photos and videos to {_pltostr(photos_dir)}..')

        for path in self.image_source.iterdir():
            basename_lower = _pltostr(path).lower()
            if (
                basename_lower.endswith(".jpg")
                or basename_lower.endswith(".jpeg")
                or basename_lower.endswith(".gif")
                or basename_lower.endswith(".mp4")
                or basename_lower.endswith(".png")
            ):
                shutil.copy(path, photos_dir / path.name)

    def gallery_init(self):
        '''
        Build up the gallery structure.

        Raises:
            RuntimeError: if there is any description

        Returns:
            bool: returns True if everything worked fine
        '''

        # create galaxy json
        if not self._create_gallery_json():
            ### TODO: Implement Error Handling
            raise RuntimeError(f'create gallery json failed for {self.name}')

        # create folder structure
        spg_common.log(f"Creating Photo Gallery {self.name}...")
        self._create_folder_structure()
        spg_common.log(f"Photo Gallery {self.name} initialized successfully!")

        return True

    def gallery_build(self, force_thumbnail_regeneration=False):
        '''
        Build the gallery (create thumbnails)

        Args:
            force_thumbnail_regeneration (bool, optional):
                Force to re-generate all thumbnails. Defaults to False.

        Raises:
            RuntimeError: will be raised if there is any error

        Returns:
            bool: returns True if everything worked fine
        '''

        gallery_config_path = _pltostr(self.gallery_config_path)
        gallery_config = spg_common.read_gallery_config(gallery_config_path)

        if not gallery_config:
            spg_common.log(f"Cannot load the gallery.json file ({gallery_config_path})!")
            ### TODO: Implement Error Handling
            raise RuntimeError

        # Get the gallery logic
        gallery_logic = get_gallery_logic(gallery_config)

        spg_common.log(f"Generating thumbnails for {self.name}...")
        gallery_logic.create_thumbnails(force_thumbnail_regeneration)

        spg_common.log(f"Generating the images_data.json file for {self.name}...")
        gallery_logic.create_images_data_file()

        spg_common.log(f"Creating the index.html for {self.name}...")
        gallery_build.build_html(gallery_config)


        spg_common.log(
            f"The gallery {self.name} was built successfully. Open {self.public_gallery_dir}"
        )

        return True

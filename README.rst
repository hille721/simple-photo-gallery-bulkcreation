.. image:: https://github.com/hille721/simple-photo-gallery-bulkcreation/actions/workflows/python-test.yml/badge.svg
    :alt: build
    :target: https://github.com/hille721/simple-photo-gallery-bulkcreation/actions/workflows/python-test.yml
.. image:: https://img.shields.io/pypi/v/simple-photo-gallery-bulkcreation.svg
    :alt: pypi
    :target: https://pypi.org/project/simple-photo-gallery-bulkcreation/

=================================
simple-photo-gallery-bulkcreation
=================================

Plugin for the `Simple Photo Gallery <https://github.com/haltakov/simple-photo-gallery>`_
which provides a config based bulk creation of multiple galleries from multiple folders of photos.

.. image:: https://raw.githubusercontent.com/hille721/simple-photo-gallery-bulkcreation/master/example/gallery_overview_example.jpg
   :alt: gallery overview

Description
===========

This plugin comes with a further command for the `Simple Photo Gallery <https://github.com/haltakov/simple-photo-gallery>`_:
:code:`gallery-bulkcreation`

Installation
============

.. code-block::

   pip install simple-photo-gallery-bulkcreation

Configuration file
==================

The configuration file is in a simple ini format.
At first there has to be a general DEFAULT section with some general settings.
Then there is one section per gallery.

.. code-block::

    [DEFAULT]
    gallery_root = example/gallery
    title = My vacations
    description = The best days of the year
    title_photo = example/pictures/mexico2017/2017-11-01_15-20-23.jpg
    title_photo_offset = 20

    [Oman 2020]
    description = Some days in the orient
    image_source = example/pictures/oman2020
    background_photo = 2020-02-02_18-40-33.jpg

    [Greece 2019]
    description = Island hoping in Greece
    image_source = example/pictures/greece2019
    background_photo = 2019-08-29_10-19-43.jpg
    background_photo_offset = 40

Usage
=====

After the creation of a `config.ini`, the creation is pretty easy via running following command:

.. code-block::

    gallery-bulkcreation config-example.ini

If everything works correctly you can preview the result, e.g. via running a simple Python server:

.. code-block::

    python3 -m http.server --directory GALLERY_ROOT/public

and then checking it in your browser under http://localhost:8000.

If you add photos to already existing galleries or add new galleries in the `config.ini` you can simple update the gallery by running the command again.


Example
=======

Check out the `example <https://github.com/hille721/simple-photo-gallery-bulkcreation/tree/master/example>`_.

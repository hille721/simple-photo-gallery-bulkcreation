=================================
simple-photo-gallery-bulkcreation
=================================

Plugin for the `Simple Photo Gallery <https://github.com/haltakov/simple-photo-gallery>`_
which provides an config based bulk creation of multiple galleries from multiple folders of photos.

Description
===========

This plugin comes with a further command for the `Simple Photo Gallery <https://github.com/haltakov/simple-photo-gallery>`_:
`gallery-bulkcreation`

Installation
============

.. code-block::

   pip install simple-photo-gallery-bulkcreation

Configuration file
==================

The configuration file is in a simple ini format.
At first there has to be a general DEFAULT section with some general setting.
Then there is one section per gallery.

.. code-block::

    [DEFAULT]
    gallery_root = /home/max/gallery
    title = Vacation
    description = The best days of the year
    title_photo = /home/max/Pictures/Mexico2017/2017-11-01_15-51-29.jpg
    title_photo_offset = 20

    [Oman 2020]
    description = Some days in the orient
    image_source = /home/max/Pictures/Oman2020
    background_photo = 2020-02-02_18-40-33.jpg
    background_photo_offset = 50

    [Greece 2019]
    description = Island hoping in Greece
    image_source = /home/max/Pictures/Greek2019
    background_photo = 2019-09-02_11-37-01.jpg

Usage
=====

.. code-block::

    gallery-bulkcreation config-example.ini
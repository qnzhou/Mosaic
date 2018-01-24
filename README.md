Mosaic Generator
================

This script is a simple mosaic generator.  It uses a random greedy algorithm to
pack as many images as possible into a canvas for a given size.

Dependencies:
-------------

The following python packages are needed:

* argparse
* PIL
* numpy

Inputs:
-------

The main input to the script is a directory of `png` images.  Ideally, each
image should have transparent background to achieve tighter packing.

Usage:
------

Assuming all input images are in `image_directory` and we would like to pack
them into a 2000px by 1800px canvas:

    ./generate_mosaic.py -W 2000 -H 1800 image_directory output.png

where `-W` and `-H` option specifies the output canvas width and height, ideally
the canvas should at least be 4x larger than a typical image in the
`image_directory`.  The scale of each image is chosen at random.  However, the
script does take a list of preferred image names from the user.  The preferred
images will be packed first and are more likely to be larger than the rest of
the images.

Examples:
---------

The following public images are generated with this script.

* Thingi10K:
* CGF Cover:

Author:
-------

Qingnan Zhou
Adobe Systems

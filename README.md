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
* json

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

The following examples are generated with this script:

[Thingi10K](https://ten-thousand-models.appspot.com):
![Thingi10K Poster](https://user-images.githubusercontent.com/3606672/65047743-fa269180-d930-11e9-8013-134764b150c1.png)

[Tetrahedral Meshing in the Wild](https://github.com/Yixin-Hu/TetWild) (Siggraph 2018):
![TetWild](https://user-images.githubusercontent.com/3606672/65047949-55f11a80-d931-11e9-809a-298af17c66ba.png)

[Decoupling Simulation Accuracy from Mesh Quality](https://dl.acm.org/citation.cfm?id=3275067) (Siggragh Asia 2018)
![Decouple](https://user-images.githubusercontent.com/3606672/65056270-94410680-d93e-11e9-9465-632dec11d598.png)

[Poly-Spline Finite Element Method](https://dl.acm.org/citation.cfm?id=3313797) (ToG 2019)
![polyfem](https://user-images.githubusercontent.com/3606672/65056678-4d9fdc00-d93f-11e9-8579-64aec46730dd.png)

[LayerCode: Optical Barcodes for 3D Printed Shapes](http://www.cs.columbia.edu/cg/layercode/) (Siggraph 2019)
![layercode](https://user-images.githubusercontent.com/3606672/65273057-48cd5a80-daee-11e9-87b8-5f21dce8e4e5.png)

Computer Graphics Forum (Volume 37 Issue 1) [Cover image](https://onlinelibrary.wiley.com/doi/10.1111/cgf.13328)

If you have used Mosaic to generate a figure, please let me know and I can include your example here.

Author:
-------

Qingnan Zhou<br>
Adobe Systems

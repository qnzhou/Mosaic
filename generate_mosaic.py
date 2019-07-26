#!/usr/bin/env python

"""
Create a random mosaic from a directory of images.
Author: Qingnan Zhou
"""

import argparse
import json
from PIL import Image
import PIL.ImageOps
import numpy as np
import numpy.random
import os
import os.path

def parse_args():
    parser = argparse.ArgumentParser(__doc__);
    parser.add_argument("--image-width", "-W", default=1024, type=int,
            help="output image width in pixels");
    parser.add_argument("--image-height", "-H", default=800, type=int,
            help="output image height in pixels");
    parser.add_argument("--mask", default=None, type=str,
            help="Masking image");
    parser.add_argument("--preferred-list", default=None, type=str,
            help="Preferred list of images that should be larger.");
    parser.add_argument("image_dir", help="A directory of images");
    parser.add_argument("output_img", help="output image name");
    return parser.parse_args();

def main():
    args = parse_args();
    out_name = os.path.splitext(args.output_img)[0];
    Image.MAX_IMAGE_PIXELS = max(Image.MAX_IMAGE_PIXELS,
            args.image_width * args.image_height + 1);
    canvas = Image.new("RGBA", (args.image_width, args.image_height),
            (0, 0, 0, 0));
    if args.mask is not None:
        mask = Image.open(args.mask);
        canvas = canvas.resize((mask.width, mask.height));
        mask = mask.convert('1');
    else:
        mask = canvas.split()[-1].convert('I');

    count = 0;
    max_num_tries = 100;
    scales = [0.5, 0.5] + [0.25] * 4 + [0.15] * 8;

    preferred = [];
    if args.preferred_list is not None:
        with open(args.preferred_list, 'r') as fin:
            for f in fin:
                preferred.append(os.path.join(args.image_dir,
                    "{}.png".format(f.strip())));
    preferred = np.unique(preferred).tolist();

    files = [];
    for fi,f in enumerate(os.listdir(args.image_dir)):
        name, ext = os.path.splitext(f);
        if ext != ".png" and ext != ".jpg": continue;
        if "{}.png".format(os.path.join(args.image_dir, name)) in preferred:
            continue;
        f = os.path.join(args.image_dir, f);
        files.append(f);

    files = preferred + numpy.random.permutation(files).tolist();
    num_preferred = len(preferred);
    image_map = {};

    for fi, f in enumerate(files):
        #f = os.path.join(args.image_dir, f);
        img = Image.open(f).convert('RGBA');
        is_preferred = fi < num_preferred;

        success = False;
        for i in range(max_num_tries):
            x,y = numpy.random.random(2);
            scale = numpy.random.choice(scales);
            if is_preferred:
                scale = min(1.0, scale * 2);
            w = int(img.width*scale);
            h = int(img.height*scale);
            resized_img = img.resize((w, h), PIL.Image.ANTIALIAS);

            cx = int(canvas.width * x);
            cy = int(canvas.height * y);
            if cx < w * 0.5 or cx > canvas.width - w * 0.5:
                continue;
            if cy < h * 0.5 or cy > canvas.height - h * 0.5:
                continue;

            box = np.array([cx-w*0.5, cy-h*0.5, cx+w*0.5, cy+h*0.5], dtype=int);
            sub_mask = mask.crop(box);
            img_mask = resized_img.split()[-1]#.convert('1');
            canvas_alpha = np.array(sub_mask, dtype=bool);
            alpha = np.array(img_mask, dtype=bool);
            composite = np.logical_and(canvas_alpha, alpha);
            if composite.any():
                ##sub_mask.save("submask_t.png");
                ##img_mask.save("imgmask_t.png");
                ##tmp = Image.fromarray(canvas_alpha, '1');
                ##tmp.save("submask.png");
                ##tmp = Image.fromarray(alpha, '1');
                ##tmp.save("imgmask.png");
                #tmp = Image.fromarray(composite, '1');
                #tmp.save("composite.png");
                #print(composite.shape);
                #print(canvas_alpha.any(), np.count_nonzero(canvas_alpha));
                #print(composite.any(), np.count_nonzero(composite));
                #print(composite.tolist());
                #assert(False);
                continue;

            canvas.paste(resized_img, box, img_mask);

            solid_image = Image.fromarray(np.ones((h,w), dtype=int) * (fi+1), "I");
            mask.paste(solid_image, box, img_mask);
            success = True;
            image_map[fi+1] = f;
            break;

        if success:
            count+=1;
            if count % 100 == 0:
                print("{} images are packed so far!".format(count));
                canvas.save(args.output_img);
                mask.save("{}_mask.png".format(out_name));
                with open("{}_index.txt".format(out_name), 'w') as fout:
                    json.dump(image_map, fout, indent=4);
        if count < fi * 0.5:
            print("Packing stopped since not enough empty space is left.");
            min_scale = scales[-1];
            if min_scale < 0.1 * scales[0]:
                break;
            scales += [min_scale * 0.5 ] * int(1.0 / min_scale)

    print("A total of {} images are packed!".format(count));
    canvas.save(args.output_img);
    mask.save("{}_mask.png".format(out_name));
    with open("{}_index.txt".format(out_name), 'w') as fout:
        json.dump(image_map, fout, indent=4);

if __name__ == "__main__":
    main();

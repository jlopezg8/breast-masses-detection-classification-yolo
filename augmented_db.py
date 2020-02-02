'''
Augmented database
==================
"We have augmented our dataset three times by rotating the mammograms with
angles of 90°, 180°, and 270°"
'''

# NOTE: this implementation could use some parallelism

import json
import os

import cv2
import numpy as np
import pydicom

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda iterable, *args, **kwargs: iter(iterable)

import conf


def save_im(im, im_abnormalities, aug_db, root, name_suffix=''):
    """Save the image to a file and store the metadata in `aug_db`."""
    im_path = f'{root}{name_suffix}.png'  # 'CBIS-DDSM/.../000000_rot90.png'
    cv2.imwrite(im_path, im)
    aug_db[im_path] = im_abnormalities
    return im, im_abnormalities


def rot_abnormalities_90(abnormalities, im):
    """Return the list of abnormalities in the image but with the bounding
    rectangles rotated 90° degrees counterclockwise.
    """
    im_h, im_w = im.shape
    rot_abnormalities = []
    for abnormality in map(dict.copy, abnormalities):
        (x, y, w, h) = abnormality['bounding_rect']
        abnormality['bounding_rect'] = (y, im_w - w - x, h, w)
        rot_abnormalities.append(abnormality)
    return rot_abnormalities


def augment_db(db):
    augmented_db = {}
    for im_path, im_abnormalities in tqdm(db.items()):
        im = pydicom.dcmread(im_path).pixel_array
        root, ext = os.path.splitext(im_path)  # 'CBIS-DDSM/.../000000', '.dcm'
        # Might as well save the original image as png:
        im, im_abnormalities = save_im(im, im_abnormalities, augmented_db, root)
        for angle in (90, 180, 270):
            # Successively rotate the image and the bounding rectangles of the
            # image abnormalities:
            im, im_abnormalities = save_im(
                np.rot90(im), rot_abnormalities_90(im_abnormalities, im),
                augmented_db, root, name_suffix=f'_rot{angle}')
    return augmented_db


def del_augmented_db():
    with open(conf.AUGMENTED_DB_PATH) as f:
        db = json.load(f)
    for im_path in db:
        os.remove(im_path)
    os.remove(conf.AUGMENTED_DB_PATH)


if __name__ == "__main__":
    if '-d' in sys.argv:  # usage: augmented_db.py -d
        del_augmented_db()
    else:
        with open(conf.ABNORMALITIES_PATH) as f:
            db = json.load(f)
        with open(conf.AUGMENTED_DB_PATH, 'w') as f:
            json.dump(augment_db(db), f, indent=4)

"""
Get the bounding rectangle and the pathology of every abnormality of every
mammogram and save the data in a JSON file.
"""

import json
import os
import sys
from collections import namedtuple

import cv2
import matplotlib.pyplot as plt
import pandas as pd
import pydicom
from tqdm import tqdm

import conf


Rect = namedtuple('Rect', ('x', 'y', 'w', 'h'))
Rect.area = lambda rect: rect.w * rect.h


def get_bounding_rect(mask_path):
    mask = pydicom.dcmread(mask_path).pixel_array
    # The mask has a depth of 16 bit. We convert it to 8 bits so OpenCV can
    # work with it:
    mask = (mask // 255).astype('uint8')
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = (Rect(*cv2.boundingRect(contour)) for contour in contours)
    return max(rects, key=Rect.area)


def get_abnormalities():
    descriptions = pd.read_csv(conf.DESCRIPTIONS_PATH)
    colnames = {'image file path': 'im_path', 'ROI mask file path': 'mask_path'}
    grouped = (descriptions.rename(columns=colnames)
                           .loc[:, ('im_path', 'mask_path', 'pathology')]
                           .groupby('im_path', sort=False))
    return {
        im_path: [
            {
                'bounding_rect': get_bounding_rect(abnormality.mask_path),
                'pathology': abnormality.pathology
            } for abnormality in im_abnormalities.itertuples()
        ] for im_path, im_abnormalities in tqdm(grouped)
    }


def show_abnormalities(im, im_abnormalities):
    color = int(im.max())
    thickness = max(im.shape) // 200
    fontScale = 5
    for abnormality in im_abnormalities:
        x, y, w, h = abnormality['bounding_rect']
        cv2.rectangle(im, (x, y), (x + w, y + h), color, thickness)
        cv2.putText(im, abnormality['pathology'], (x, y - 2 * thickness),
                    cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thickness)
    plt.imshow(im, cmap='gray')
    plt.show()


def read_im_and_abnormalities(im_path):
    root, ext = os.path.splitext(im_path)
    if ext == '.dcm':
        im = pydicom.dcmread(im_path).pixel_array
        abnormalities_path = conf.ABNORMALITIES_PATH
    else:
        im = cv2.imread(im_path)
        abnormalities_path = conf.AUGMENTED_DB_PATH
    with open(abnormalities_path) as f:
        abnormalities = json.load(f)
    return im, abnormalities[im_path]


if __name__ == "__main__":
    if len(sys.argv) == 2:  # usage: get_abnormalities.py IM_PATH
        im, abnormalities = read_im_and_abnormalities(im_path=sys.argv[1])
        show_abnormalities(im, abnormalities)
    else:
        abnormalities = get_abnormalities()
        with open(conf.ABNORMALITIES_PATH, 'w') as f:
            json.dump(abnormalities, f, indent=4)

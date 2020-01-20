"""
Get the bounding rectangle and the pathology of every abnormality of every
mammogram and save the data in a JSON file.
"""

import json
import sys
from collections import namedtuple

import cv2
import matplotlib.pyplot as plt
import pandas as pd
import pydicom
from tqdm import tqdm


DESCRIPTIONS_PATH = 'mammograms_descriptions2.csv'
ABNORMALITIES_PATH = 'abnormalities.json'

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
    descriptions = pd.read_csv(DESCRIPTIONS_PATH)
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


def show_abnormalities(im_path):
    with open(ABNORMALITIES_PATH) as f:
        abnormalities = json.load(f)
    im = pydicom.dcmread(im_path).pixel_array
    color = int(im.max())
    thickness = max(im.shape) // 200
    fontScale = 5
    for abnormality in abnormalities[im_path]:
        x, y, w, h = abnormality['bounding_rect']
        cv2.rectangle(im, (x, y), (x + w, y + h), color, thickness)
        cv2.putText(im, abnormality['pathology'], (x, y - 2 * thickness),
                    cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thickness)
    plt.imshow(im, cmap='gray')
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) == 2:  # usage: get_abnormalities.py IM_PATH
        show_abnormalities(im_path=sys.argv[1])
    else:
        with open(ABNORMALITIES_PATH, 'w') as f:
            json.dump(get_abnormalities(), f, indent=4)

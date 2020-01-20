"""
The images, cropped images and ROI masks file paths in the descriptions don't
match the paths in our copy of the dataset, so we replace the paths in the
description with the paths in our dataset.
"""

import os
from glob import glob, iglob

import pandas as pd

import conf


IM_PATH_COLNAME = 'image file path'
CROPPED_PATH_COLNAME = 'cropped image file path'
MASK_PATH_COLNAME = 'ROI mask file path'


def find_im(path):
    # path = 'Mass-Training_P_00001_LEFT_CC/1.3.6.1.4.1.9590.100.1.2.422112722213189649807611434612228974994/1.3.6.1.4.1.9590.100.1.2.342386194811267636608694132590482924515/000000.dcm'
    components = path.split('/')
    root = components[0]
    basename = components[-1]
    real_path = next(  # just need the first path found
        iglob(os.path.join(conf.DATASET_PATH, root, '**', basename),
              # 'CBIS-DDSM/**/Mass-Training_P_00001_LEFT_CC/**/000000.dcm'
              recursive=True))
    return real_path


def find_overlay_ims(paths):
    """Return the real paths for the cropped image and ROI mask of a given
    abnormality.
    
    `paths` is a ``pandas.Series`` containing the cropped image and ROI mask paths.

    Return a tuple ``(real_cropped_path, real_mask_path)``.
    """
    root = paths[CROPPED_PATH_COLNAME].split('/')[0]
    path0, path1 = glob(os.path.join(conf.DATASET_PATH, root, '**', '*.dcm'),
                        recursive=True)
    # The cropped image is smaller than the ROI mask:
    path0_is_cropped = os.path.getsize(path0) < os.path.getsize(path1)
    return (path0, path1) if path0_is_cropped else (path1, path0)


descriptions = pd.read_csv(conf.DESCRIPTIONS_PATH)
descriptions[IM_PATH_COLNAME] = descriptions[IM_PATH_COLNAME].map(find_im)
colnames = (CROPPED_PATH_COLNAME, MASK_PATH_COLNAME)
descriptions.loc[:, colnames] = (
    descriptions.loc[:, colnames].apply(find_overlay_ims, axis=1,
                                        result_type='broadcast'))
descriptions.to_csv(conf.DESCRIPTIONS_PATH)

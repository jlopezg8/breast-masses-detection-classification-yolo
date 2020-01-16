'''
Original database
=================
"We have randomly selected a set of 600 mammograms from DDSM database which
are equally categorized to benign and malignant cases."
'''

import numpy as np
import pandas as pd

DDSM_DB = pd.read_csv('CBIS-DDSM/mass_case_description_train_set.csv')

malign_indices = DDSM_DB.pathology == 'MALIGNANT'
benign_indices = ~malign_indices

"""The descriptions have, for a given mammogram, as many rows as there are
abnormalities found in it, so we remove the duplicates before sampling.

Also, there are mammograms in which both benign and malign abnormalities were
found, so we perform a set difference on the largest set before sampling.
"""

IM_PATH_COLNAME = 'image file path'
malign_im_paths = DDSM_DB.loc[malign_indices, IM_PATH_COLNAME].unique()
benign_im_paths = DDSM_DB.loc[benign_indices, IM_PATH_COLNAME].unique()
benign_im_paths = np.setdiff1d(benign_im_paths, malign_im_paths,
                               assume_unique=True)

rand = np.random.RandomState(seed=1)  # for reproducibility
malign_samples = rand.choice(malign_im_paths, 300, replace=False)
benign_samples = rand.choice(benign_im_paths, 300, replace=False)
samples = np.concatenate((malign_samples, benign_samples))

mammograms = DDSM_DB.merge(pd.Series(samples, name=IM_PATH_COLNAME))
assert len(mammograms[IM_PATH_COLNAME].unique()) == 600
mammograms.to_csv('mammograms_descriptions.csv')

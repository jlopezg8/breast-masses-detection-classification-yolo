"""
Paths and other configuration properties.
"""

import contextlib
import os

# Path to the Mass-Training-Description (csv):
MASS_TRAIN_DESCRIPTION_PATH = r'CBIS-DDSM\mass_case_description_train_set.csv'

# *Immediate* parent directory of the cases directories:
DATASET_PATH = r'CBIS-DDSM\Train\Mass'

# These files are created by the scripts. No need to modify these:
with contextlib.suppress(FileExistsError):
    os.mkdir('metadata')
DESCRIPTIONS_PATH = os.path.join('metadata', 'mammograms_descriptions.csv')
ABNORMALITIES_PATH = os.path.join('metadata', 'abnormalities.json')
AUGMENTED_DB_PATH = os.path.join('metadata', 'augmented_db.json')

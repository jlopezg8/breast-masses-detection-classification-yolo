"""We have randomly selected a set of 600 mammograms from DDSM database which
are equally categorized to benign and malignant cases.
"""

import pandas as pd

DDSM_DB = pd.read_csv('CBIS-DDSM/mass_case_description_train_set.csv')
malign_indices = DDSM_DB.pathology == 'MALIGNANT'
benign_indices = ~malign_indices
# Set *random_state* for reproducibility:
malign_samples = DDSM_DB[malign_indices].sample(300, random_state=1)
benign_samples = DDSM_DB[benign_indices].sample(300, random_state=1)
mammograms = pd.concat((malign_samples, benign_samples))
mammograms.to_csv('mammograms_descriptions.csv')

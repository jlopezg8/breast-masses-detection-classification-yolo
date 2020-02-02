Implementation of Al-masni, M. A., Al-antari, M. A., Park, J. M., Gi, G., Kim,
T. Y., Rivera, P., Valarezo, E., Choi, M. T., Han, S. M., & Kim, T. S. (2018).
Simultaneous detection and classification of breast masses in digital
mammograms via a deep learning YOLO-based CAD system. Computer Methods and
Programs in Biomedicine, 157, 85–94. https://doi.org/10.1016/j.cmpb.2018.01.017

## Usage

1. Download the Mass-Training Full Mammogram Images, ROI and Cropped Images,
and Description from the [CBIS-DDSM](https://wiki.cancerimagingarchive.net/display/Public/CBIS-DDSM#5e40bd1f79d64f04b40cac57ceca9272).
2. Clone or download this repository.
3. Install this project's dependencies, ideally within a [virtual environment](https://virtualenv.pypa.io/en/latest/), running the following command from the
project's root directory:
    ````cmd
    pip install -r requirements.txt
    ````
4. Set the required paths to the CBIS-DDSM in `conf.py`.
5. Run `original_db.py`.
6. Run `replace_paths.py` if the images paths in your copy of the CBIS-DDSM
don't match the paths in the description csv file.
7. Run `get_abnormalities.py`.
8. Run `augmented_db.py`.
9. ...

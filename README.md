# Surveying the Deep: A Review of Computer Vision in the Benthos

This repository hosts the code used to reproduce figures found in the paper [_Surveying the Deep: A Review of Computer Vision in the Benthos_ (Trotter _et al._ 2025)](https://doi.org/10.1016/j.ecoinf.2024.102989). For this paper, two figures (Figure 1 and Figure 7) were generated programmatically. The code is provided here for reproducibility purposes.

## Instructions
To reproduce the aformentioned figures, please follow these steps.

### 1. Download the required CSV files
Download both the paper techniques ([link](https://ars.els-cdn.com/content/image/1-s2.0-S1574954124005314-mmc2.csv)) and literature latitude and longitude ([link](https://ars.els-cdn.com/content/image/1-s2.0-S1574954124005314-mmc1.csv)) CSV files from the paper's supplementary material. The former CSV is used to generate Figure 1, and the latter is used to generate Figure 7.

### 2. Generate a Python environment
Generate a Python environment using `requirements.yaml`. This was generated using [mamba](https://github.com/mamba-org/mamba), so it is recommended you also use this to create the environment. If you don't want to use a virtual environment, provided you have [geopandas==0.14.4](https://geopandas.org/en/stable/) and its dependencies installed, the code _should_ work. The code has been tested with Python 3.13.1.

```bash
mamba env create --file requirements.yaml
mamba activate surveying_the_deep
```

### 3. Run the code

To reproduce Figure 1, showing the progression of computer vision-based benthic biodiversity monitoring literature over time, run:

```bash
python3 techniques.py /path/to/techniques.csv $output_path                         
```         

To reproduce Figure 7, showing the geographic origin of image data used to train the reviewed automated benthic image analysis systems, run:

```bash
python3 heatmap.py /path/to/lat_longs.csv $output_path
```
Running both scripts without optional arguments will produce the figures as they appear in the paper. Optional arguments are provided for customisation, please see the help message of each script for more information.

```bash
python3 techniques.py --help
python3 heatmap.py --help
```

## Citation

```
@article{trotterSurveyingDeepReview2025,
  title = {Surveying the Deep: {{A}} Review of Computer Vision in the Benthos},
  shorttitle = {Surveying the Deep},
  author = {Trotter, Cameron and Griffiths, Huw J. and Whittle, Rowan J.},
  year = {2025},
  journal = {Ecological Informatics},
  pages = {102989},
  issn = {15749541},
  doi = {10.1016/j.ecoinf.2024.102989}
```

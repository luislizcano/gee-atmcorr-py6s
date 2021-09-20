# Multi-Sensor Atmospheric Correction in Google Earth Engine [Python API]

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fluislizcano%2Fgee-atmcorr-py6s%2F&count_bg=%2379C83D&title_bg=%23555555&icon=nextdoor.svg&icon_color=%23E7E7E7&title=Visits&edge_flat=false)](https://hits.seeyoufarm.com)
[![GPL license](https://img.shields.io/badge/License-GPL-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/luislizcano/gee-atmcorr-py6s/blob/main/jupyter_notebooks/BOA_by_collection_colab.ipynb)
[![DOI](https://zenodo.org/badge/304372687.svg)](https://zenodo.org/badge/latestdoi/304372687)


**Description:** This script allows to do atmospheric correction for list of images (or individual images) of Sentinel-2 and Landsat sensors, especifically for images over coastal or oceanic areas, using the GEE Python API in Jupyter Notebook. Some atmospheric correction settings can be modified in the *parameters.py* module to work with images over inland areas (See line 36 in that module). The script does AC automatically by providing the right satellite mission, list of image ID's, and a specific GEE Asset to export processed images to your personal GEE account.<br/>

More sensors can be added by modifying the *mission_specifics.py* and *parameters.py* modules to properly work with the available collections in GEE and [Py6S](https://github.com/robintw/Py6S/blob/master/Py6S/Params/wavelength.py).<br/>

Script modified from https://github.com/samsammurphy/gee-atmcorr-S2<br/>
By Luis Lizcano-Sandoval<br/>
College of Marine Science, University of South Florida<br/>
luislizcanos@usf.edu<br/>
Created: 10/30/2020<br/>
Updated: 09/02/2021

## Sentinel-2 Image Before:
<img src="https://raw.github.com/luislizcano/gee-atmcorr-py6s/main/jupyter_notebooks/toa.png" width="800">

## Sentinel-2 Image After:
<img src="https://raw.github.com/luislizcano/gee-atmcorr-py6s/main/jupyter_notebooks/boa.png" width="800">

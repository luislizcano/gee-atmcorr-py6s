# gee-atmcorr-py6s
Multi-Sensor Atmospheric Correction in Google Earth Engine [Python API]

Description: These Jupyter scripts allows to do atmospheric correction for a single image or a list of images (colelction) of Sentinel-2 and Landsat sensors (8-7-5), especifically for images over coastal or oceanic areas. These settings can be modified from the parameters.py module to work with images over inland areas (See line 36 in that module). The script does AC automatically, the user only needs to provide the right mission, imageID, and specific assetID to export the processed image to your EE Assets.
More sensors can be added by modifying the mission_specifics.py and parameters.py modules to properly work with the available collections in GEE and Py6S.

Script modified from https://github.com/samsammurphy/gee-atmcorr-S2

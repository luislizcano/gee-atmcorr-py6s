"""
mission_specifics.py, Sam Murphy (2017-06-28)

Information on satellite missions stored here (e.g. wavebands, etc.)

Modified by Luis Lizcano-Sandoval
College of Marine Science, University of South Florida
09-28-2020
"""

import ee


def ee_bandnames(mission):
    """
    visible to short-wave infrared wavebands (EarthEngine nomenclature)

    notes:
    [1] skipped Landsat7 'PAN' to fit Py6S
    [2] thermal bands in L7, L5 & L4 are not used in Py6S.
    """

    switch = {
        'Sentinel-2A':['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B10','B11','B12'],
        'Sentinel-2B':['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B10','B11','B12'],
        'Landsat8':['B1','B2','B3','B4','B5','B6','B7','B8','B9'],
        'Landsat7':['B1','B2','B3','B4','B5','B7'],
        'Landsat5':['B1','B2','B3','B4','B5','B7'],
        'Landsat4':['B1','B2','B3','B4','B5','B7']
    }

    return switch[mission]

def py6s_bandnames(mission):
    """
    visible to short-wave infrared wavebands (Py6S nomenclature)

    notes: 
    [1] Landsat8 'B8' === 'PAN'
    [2] Landsat7 'PAN' is missing?

    """

    switch = {
        'Sentinel-2A':['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B10','B11','B12'],
        'Sentinel-2B':['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B10','B11','B12'],
        'Landsat8':['B1','B2','B3','B4','B5','B6','B7','B8','B9'],
        'Landsat7':['B1','B2','B3','B4','B5','B7'],
        'Landsat5':['B1','B2','B3','B4','B5','B7'],
        'Landsat4':['B1','B2','B3','B4','B5','B7']
    }

    return switch[mission]

def common_bandnames(mission):
    """
    visible to short-wave infrared wavebands (common bandnames)
    """

    switch = {
        'Sentinel-2A':['aerosol','blue','green','red',
        'redEdge1','redEdge2','redEdge3','nir','redEdge4',
        'waterVapour','cirrus','swir1','swir2'],
        'Sentinel-2B':['aerosol','blue','green','red',
        'redEdge1','redEdge2','redEdge3','nir','redEdge4',
        'waterVapour','cirrus','swir1','swir2'],
        'Landsat8':['aerosol','blue','green','red','nir','swir1','swir2','pan','cirrus'],
        'Landsat7':['blue','green','red','nir','swir1','swir2'],
        'Landsat5':['blue','green','red','nir','swir1','swir2'],
        'Landsat4':['blue','green','red','nir','swir1','swir2']
    }

    return switch[mission]

def py6S_sensor(image,mission):
    """
    Py6S satellite_sensor name from satellite mission name.
    *Modified to match either Sentinel-2A or Sentinel-2B.
    """
    switch = {
        'Sentinel-2A':'S2A_MSI',
        'Sentinel-2B':'S2B_MSI',
        'Landsat8':'LANDSAT_OLI',
        'Landsat7':'LANDSAT_ETM',
        'Landsat5':'LANDSAT_TM',
        'Landsat4':'LANDSAT_TM'
    }
    return switch[mission]

def eeCollection(mission):
    """
    Earth Engine image collection name from satellite mission name
    """

    switch = {
        'Sentinel2':'COPERNICUS/S2',
        'Landsat8':'LANDSAT/LC08/C01/T1_TOA',
        'Landsat7':'LANDSAT/LE07/C01/T1_TOA',
        'Landsat5':'LANDSAT/LT05/C01/T1_TOA',
        'Landsat4':'LANDSAT/LT04/C01/T1_TOA'
    }

    return switch[mission]

def sunAngleFilter(mission):
    """
    Sun angle filter avoids where elevation < 15 degrees
    """
  
    switch = {
        'Sentinel-2A':ee.Filter.lt('MEAN_SOLAR_ZENITH_ANGLE',75),
        'Sentinel-2B':ee.Filter.lt('MEAN_SOLAR_ZENITH_ANGLE',75),
        'Landsat8':ee.Filter.gt('SUN_ELEVATION',15),
        'Landsat7':ee.Filter.gt('SUN_ELEVATION',15),
        'Landsat5':ee.Filter.gt('SUN_ELEVATION',15),
        'Landsat4':ee.Filter.gt('SUN_ELEVATION',15)
    }

    return switch[mission]

def ESUNs(image, mission, band):
    """
    ESUN (Exoatmospheric spectral irradiance)

    References
    ----------

    Landsat 4  [1]
    Landsat 5  [1]
    Landsat 7  [1]
    Landsat 8  [2]


    [1] Chander et al. (2009) Summary of current radiometric calibration
        coefficients for Landsat MSS, TM, ETM+, and EO-1 ALI sensors.
        Remote Sensing of Environment. 113, 898-903

    [2] Benjamin Leutner (https://github.com/bleutner/RStoolbox)
    """
  
    # For Sentinel-2:
    Sentinel2 = []
    if 'Sentinel' in mission:
        Sentinel2 =  float(image.get('SOLAR_IRRADIANCE_' + band).getInfo())
    
    # Coefficients for Landsat:
    esunL8 = {
        'B1': 1895.33, 
        'B2': 2004.57, 
        'B3': 1820.75, 
        'B4': 1549.49, 
        'B5': 951.76, 
        'B6': 247.55, 
        'B7': 85.46, 
        'B8': 1723.8, 
        'B9': 366.97
    }
    esunL7 = {
        'B1': 1997, 
        'B2': 1812, 
        'B3': 1533, 
        'B4': 1039, 
        'B5': 230.8, 
        'B7': 84.9, 
    }
    esunL5 = {
        'B1': 1983, 
        'B2': 1796, 
        'B3': 1536, 
        'B4': 1031, 
        'B5': 220, 
        'B7': 83.44, 
    }    
    esunL4 = {
        'B1': 1983, 
        'B2': 1795, 
        'B3': 1539, 
        'B4': 1028, 
        'B5': 219.8, 
        'B7': 83.49, 
    }
    
    # Get the coefficient at the specified band:
    Landsat8 = []
    Landsat7 = [] # PAN =  1362 (removed to match Py6S)
    Landsat5 = []
    Landsat4 = []
    if 'Landsat8' in mission:
        Landsat8 = esunL8[band]
    elif 'Landsat7' in mission:
        Landsat7 = esunL7[band] # PAN =  1362 (removed to match Py6S)
    elif 'Landsat5' in mission:
        Landsat5 = esunL5[band]
    elif 'Landsat4' in mission:
        Landsat4 = esunL4[band]
    
    switch = {
        'Sentinel-2A':Sentinel2,
        'Sentinel-2B':Sentinel2,
        'Landsat8':Landsat8,
        'Landsat7':Landsat7,
        'Landsat5':Landsat5,
        'Landsat4':Landsat4
    }

    return switch[mission]

def solar_z(image, mission):
    """
    solar zenith angle (degrees)
    """

    def sentinel2(image):
        return image.get('MEAN_SOLAR_ZENITH_ANGLE').getInfo()
  
    def landsat(image):
        return ee.Number(90).subtract(image.get('SUN_ELEVATION')).getInfo()
  
    switch = {
        'Sentinel-2A':sentinel2,
        'Sentinel-2B':sentinel2,
        'Landsat8':landsat,
        'Landsat7':landsat,
        'Landsat5':landsat,
        'Landsat4':landsat
    }

    getSolarZenith = switch[mission]

    return getSolarZenith(image)


def cloud_cover(mission):
    """
    cloud cover percentage
    """

    cloud_S2 = ['CLOUDY_PIXEL_PERCENTAGE']
  
    cloudLandsat = ['CLOUD_COVER']
  
    switch = {
        'Sentinel-2A':cloud_S2,
        'Sentinel-2B':cloud_S2,
        'Landsat8':cloudLandsat,
        'Landsat7':cloudLandsat,
        'Landsat5':cloudLandsat,
        'Landsat4':cloudLandsat
    }

    getCloudCover = switch[mission]

    return getCloudCover


def TOA(image, mission):

    switch = {
        'Sentinel-2A':image.divide(10000).set(image.toDictionary(image.propertyNames())),
        'Sentinel-2B':image.divide(10000).set(image.toDictionary(image.propertyNames())),
        'Landsat8':image,
        'Landsat7':image,
        'Landsat5':image,
        'Landsat4':image
    }

    return switch[mission]
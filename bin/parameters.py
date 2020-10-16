"""
Required parameters that changes among satellites:
Set of parameters for atmospheric correction
Adapted from Sam Murphy
By Luis Lizcano-Sandoval
09/28/2020
"""

import ee
from Py6S import *
import datetime
import math
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.getcwd()),'bin'))
from atmospheric import Atmospheric
import mission_specifics as mn

def BOA(mission,image,bandname):
    
    ##Load set of parameters:
    image = ee.Image(image)
    sensor = mn.py6S_sensor(image,mission)
        
    # Top of atmosphere reflectance:
    toa = mn.TOA(image,mission)
    
    # Date in python format:
    info = ee.Image(image).getInfo()['properties']
    py_date = datetime.datetime.utcfromtimestamp(info['system:time_start']/1000)# i.e. Python uses seconds, EE uses milliseconds

    # Solar zenith angle:
    solar_z = mn.solar_z(image,mission)

    # Target altitude:
    ####Uncomment the next three lines if want to do AC to images over land.####
    #SRTM = ee.Image('CGIAR/SRTM90_V4')# Shuttle Radar Topography mission covers *most* of the Earth
    #alt = SRTM.reduceRegion(reducer = ee.Reducer.mean(),geometry = imgCentroid).get('elevation').getInfo()
    #km = alt/1000 # i.e. Py6S uses units of kilometers
    km = 0.001 #Set to 1m due to we are only interested in coastal water, not land.

    # Date used for the Atmospheric correction functions, in GEE format:
    ee_date = ee.Date(image.get('system:time_start'))

    # Get the centroid coordinates of the image:
    imgGeometry = image.geometry().buffer(10)
    imgCentroid = imgGeometry.centroid()
    coord = imgCentroid.getInfo()['coordinates'] #point only

    # Predefined atmospheric constituents:
    h2o = Atmospheric.water(imgCentroid,ee_date).getInfo()   #Water\
    o3 = Atmospheric.ozone(imgCentroid,ee_date).getInfo()    #Ozone\
    aot = Atmospheric.aerosol(imgCentroid,ee_date).getInfo() #Aerosols

    # Instantiate
    s = SixS()

    # Atmospheric constituents\n",
    s.atmos_profile = AtmosProfile.UserWaterAndOzone(h2o,o3)
    s.aero_profile = AeroProfile.Continental
    s.aot550 = aot

    # Earth-Sun-satellite geometry
    s.geometry = Geometry.User()
    s.geometry.view_z = 9            # For Sentinel is ~10° and Landsat ~7.5°. So, 9° is in between both. (Roy et al. 2017. https://doi.org/10.1016/j.rse.2017.06.019)
    s.geometry.solar_z = solar_z     # solar zenith angle
    s.geometry.month = py_date.month # month and day used for Earth-Sun distance
    s.geometry.day = py_date.day     # month and day used for Earth-Sun distance
    s.altitudes.set_sensor_satellite_level()
    s.altitudes.set_target_custom_altitude(km) ## Target at Sea level (0.001 km)


    def spectralResponseFunction(bandname):

        #Extract spectral response function for given band name
        
        if 'S2A_MSI' == sensor:
            bandSelect = {
                'B1':PredefinedWavelengths.S2A_MSI_01,
                'B2':PredefinedWavelengths.S2A_MSI_02,
                'B3':PredefinedWavelengths.S2A_MSI_03,
                'B4':PredefinedWavelengths.S2A_MSI_04,
                'B5':PredefinedWavelengths.S2A_MSI_05,
                'B6':PredefinedWavelengths.S2A_MSI_06,
                'B7':PredefinedWavelengths.S2A_MSI_07,
                'B8':PredefinedWavelengths.S2A_MSI_08,
                'B8A':PredefinedWavelengths.S2A_MSI_8A,
                'B9':PredefinedWavelengths.S2A_MSI_09,
                'B10':PredefinedWavelengths.S2A_MSI_10,
                'B11':PredefinedWavelengths.S2A_MSI_11,
                'B12':PredefinedWavelengths.S2A_MSI_12
                }
        elif 'S2B_MSI' == sensor:
            bandSelect = {
                'B1':PredefinedWavelengths.S2B_MSI_01,
                'B2':PredefinedWavelengths.S2B_MSI_02,
                'B3':PredefinedWavelengths.S2B_MSI_03,
                'B4':PredefinedWavelengths.S2B_MSI_04,
                'B5':PredefinedWavelengths.S2B_MSI_05,
                'B6':PredefinedWavelengths.S2B_MSI_06,
                'B7':PredefinedWavelengths.S2B_MSI_07,
                'B8':PredefinedWavelengths.S2B_MSI_08,
                'B8A':PredefinedWavelengths.S2B_MSI_8A,
                'B9':PredefinedWavelengths.S2B_MSI_09,
                'B10':PredefinedWavelengths.S2B_MSI_10,
                'B11':PredefinedWavelengths.S2B_MSI_11,
                'B12':PredefinedWavelengths.S2B_MSI_12
                }
        elif 'LANDSAT_OLI' == sensor:
            bandSelect = {
                'B1':PredefinedWavelengths.LANDSAT_OLI_B1,
                'B2':PredefinedWavelengths.LANDSAT_OLI_B2,
                'B3':PredefinedWavelengths.LANDSAT_OLI_B3,
                'B4':PredefinedWavelengths.LANDSAT_OLI_B4,
                'B5':PredefinedWavelengths.LANDSAT_OLI_B5,
                'B6':PredefinedWavelengths.LANDSAT_OLI_B6,
                'B7':PredefinedWavelengths.LANDSAT_OLI_B7,
                'B8':PredefinedWavelengths.LANDSAT_OLI_B8,
                'B9':PredefinedWavelengths.LANDSAT_OLI_B9
                }
        elif 'LANDSAT_ETM' == sensor:
            bandSelect = {
                'B1':PredefinedWavelengths.LANDSAT_ETM_B1,
                'B2':PredefinedWavelengths.LANDSAT_ETM_B2,
                'B3':PredefinedWavelengths.LANDSAT_ETM_B3,
                'B4':PredefinedWavelengths.LANDSAT_ETM_B4,
                'B5':PredefinedWavelengths.LANDSAT_ETM_B5,
                'B7':PredefinedWavelengths.LANDSAT_ETM_B7
                }
        elif 'LANDSAT_TM' == sensor:
            bandSelect = {
                'B1':PredefinedWavelengths.LANDSAT_TM_B1,
                'B2':PredefinedWavelengths.LANDSAT_TM_B2,
                'B3':PredefinedWavelengths.LANDSAT_TM_B3,
                'B4':PredefinedWavelengths.LANDSAT_TM_B4,
                'B5':PredefinedWavelengths.LANDSAT_TM_B5,
                'B7':PredefinedWavelengths.LANDSAT_TM_B7
                }

        return Wavelength(bandSelect[bandname])

    def toa_to_rad(bandname):
        
        #Converts top of atmosphere reflectance to at-sensor radiance"
        
        # solar exoatmospheric spectral irradiance
        ESUN = mn.ESUNs(image,mission,bandname)
        solar_angle_correction = math.cos(math.radians(solar_z))

        # Earth-Sun distance (from day of year)
        doy = py_date.timetuple().tm_yday
        # http://physics.stackexchange.com/questions/177949/earth-sun-distance-on-a-given-day-of-the-year
        d = 1 - 0.01672 * math.cos(0.9856 * (doy-4)) 

        # conversion factor
        multiplier = ESUN*solar_angle_correction/(math.pi*d**2)

        # at-sensor radiance
        rad = toa.select(bandname).multiply(multiplier)
    
        return rad
    

    def surface_reflectance(bandname):
        
        #Calculate surface reflectance from at-sensor radiance given waveband name"
         
        # run 6S for this waveband
        s.wavelength = spectralResponseFunction(bandname)
        s.run()
    
        # extract 6S outputs
        Edir = s.outputs.direct_solar_irradiance             #direct solar irradiance
        Edif = s.outputs.diffuse_solar_irradiance            #diffuse solar irradiance
        Lp   = s.outputs.atmospheric_intrinsic_radiance      #path radiance
        absorb  = s.outputs.trans['global_gas'].upward       #absorption transmissivity
        scatter = s.outputs.trans['total_scattering'].upward #scattering transmissivity
        tau2 = absorb*scatter                                #total transmissivity

        # radiance to surface reflectance
        rad = toa_to_rad(bandname)
        ref = rad.subtract(Lp).multiply(math.pi).divide(tau2*(Edir+Edif))

        return ref
    
#     ## Function to get band scales
        ##Update: It does not make sense to run these function to rescale bands,
        ## because when the image is exported to Assets will be resampled to minimum res.
#     def band_scale(bandname):
        
#         if 'S2A_MSI' == sensor:
#             bandRes = {
#                 'B1':60,
#                 'B2':10,
#                 'B3':10,
#                 'B4':10,
#                 'B5':20,
#                 'B6':20,
#                 'B7':20,
#                 'B8':10,
#                 'B8A':20,
#                 'B9':60,
#                 'B10':60,
#                 'B11':20,
#                 'B12':20
#                 }
#         elif 'S2B_MSI' == sensor:
#             bandRes = {
#                 'B1':60,
#                 'B2':10,
#                 'B3':10,
#                 'B4':10,
#                 'B5':20,
#                 'B6':20,
#                 'B7':20,
#                 'B8':10,
#                 'B8A':20,
#                 'B9':60,
#                 'B10':60,
#                 'B11':20,
#                 'B12':20
#                 }
#         elif 'LANDSAT_OLI' == sensor:
#             bandRes = {
#                 'B1':30,
#                 'B2':30,
#                 'B3':30,
#                 'B4':30,
#                 'B5':30,
#                 'B6':30,
#                 'B7':30,
#                 'B8':15,
#                 'B9':15
#                 }
#         elif 'LANDSAT_ETM' == sensor:
#             bandRes = {
#                 'B1':30,
#                 'B2':30,
#                 'B3':30,
#                 'B4':30,
#                 'B5':30,
#                 'B7':30
#                 }
#         elif 'LANDSAT_TM' == sensor:
#             bandRes = {
#                 'B1':30,
#                 'B2':30,
#                 'B3':30,
#                 'B4':30,
#                 'B5':30,
#                 'B7':30
#                 }

#         return (bandRes[bandname])
    
#     ## Function for resampling bands
#     def resample(sr):
#         ## Display a bilinear resampled image with 10m pixel spacing.
#         band = sr.select(bandname)
#         proj = band.projection()
#         bandScale = band_scale(bandname)
#         resample = sr.resample('bilinear').reproject({\
#                 'crs': proj,
#                 'scale': bandScale,
#                 });
#         return resample
    
    
    
    sr = surface_reflectance(bandname)
#     sr_resample = resample(sr)
    
    
    return sr

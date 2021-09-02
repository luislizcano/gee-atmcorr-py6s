"""
Function to apply atmospheric correction to
a predefine set of bands.
By Luis Lizcano-Sandoval
09/02/2021
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.getcwd()),'bin'))
import ee
import mission_specifics as mn
from parameters import BOA

## The collection, mission, bands AND imageID arguments are defined in the main script.

def getBOA(collection, mission, bands, imageID):
    List = collection.toList(collection.size())
    Size = List.size().getInfo()
    boaColl = ee.ImageCollection([])
    
    for i in range(Size):
        get = imageID[i]
             
        img = ee.Image(mn.eeCollection(mission) + '/'+ get)
        imgInfo= ee.Image(img)        
        print('Processing Image '+str(i+1)+':', img.getInfo()['properties']['system:index'])
        
        ## Extract QA and thermal bands for Landsat
        qa = []
        if 'Sentinel' in mission:
            qa = img.select('QA60')#For Sentinel
        elif 'Landsat8' in mission:
            qa = img.select('BQA') #For Landsat-8
            thermal = img.select('B10')
        elif 'Landsat7' in mission:
            qa = img.select('BQA') #For Landsat7
            thermal = img.select('B6_VCID_1')
        else:
            qa = img.select('BQA') #For Landsat5/4
            thermal = img.select('B6')
        
        if 'Sentinel' in mission:
            mission2 = str(img.getInfo()['properties']['SPACECRAFT_NAME'])
            print('Mission: ', mission2)
        
        ## Create an empty image. It will have a band called 'constant' that is removed below.
        output = ee.Image()
        
        for i in range(len(bands)):
            ## Get BOA reflectance for the respective band.
            if 'Sentinel' in mission:
                b = BOA(mission2, img, bands[i])
            else:
                b = BOA(mission, img, bands[i])

            ## The function *positive* will convert any negative value to 0.0001 in all bands. 
            ## For Sentinel-2, the bands B1,B2,B3,B4 are more susceptible to present negative 
            ## values in very dark/coastal areas. I have compared those areas using Sentinel-2 L2A 
            ## images and it seems they do the same: dark areas showing default minimum valid pixel 
            ## values of 0.0001. 
            def positive(band):
                    ## If there are masked areas, unmask them and assign a specific pixel value different from 0.0001.
                    ## Sometimes Sentinel-2 tiles present cut off corners.
                    unmasked = band.unmask(9999)

                    ## Take all the positive pixel values and assing 0.0001 values to all negative ones.
                    b = unmasked.gt(0)
                    b_mask = unmasked.mask(b)
                    b_unmasked = b_mask.unmask(0.0001)

                    ## Re-mask the areas with 9999 values
                    remask = b_unmasked.neq(9999)

                    return ee.Image(b_unmasked).mask(remask)

            ## Bands to convert to positive.
            bPos = positive(b)

            ## Getting all the bands together
            output = output.addBands(bPos)
 
        ## Remove the 'constant' band
        output = output.select(output.bandNames().remove('constant'))
        
        ## Add thermal band if this is a Landsat image
        if 'Landsat' in mission:
            output = output.addBands(thermal)
        
        ## Add QA bands
        output = output.addBands(qa)

                
        ## Copy properties from the original image
        output = output.set(img.toDictionary(img.propertyNames()))
            
        #print('Processed Image '+str(i)+':', output.getInfo()['properties']['system:index'])
        print('Done!')
        
        boaColl = boaColl.merge(ee.ImageCollection(output))
    
    return boaColl
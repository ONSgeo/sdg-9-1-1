[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

## Introduction

The Sustainable Development Goals (SDGs) are part of the UN 2030 Agenda for Sustainable Development. The Office for National Statistics (ONS) reports the UK data for the SDG indicators on the [UK Sustainable Development Goals webpage](https://sdgdata.gov.uk/), contributing to progress towards a sustainable global future. 

Included in the 17 SDGs is Goal 9, which aims to ["Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation"](https://sdgs.un.org/goals/goal9). One indicator that supports this goal is **9.1.1: Proportion of the rural population who live within 2km of an all-season road**. This is commonly known as the Rural-Access Index (RAI). 

This code aims to provide an automated calculation of SDG indicator 9.1.1 for the timely reporting on progress towards Goal 9. The most recent reporting of this indicator by the UK covers the year [2011](https://sdgdata.gov.uk/9-1-1/).

## Set-up 
?
1. Clone this repository into the directory you'd like to work from. 
    
2. Create a .env file to set the directory from which inputs will be imported and results will be exported:

   Open the Notepad app and write ROOT_DIR= followed by the directory in which the input data is stored (and results we be exported to),  eg: 
    
    ROOT_DIR=C:\Users\username\scripts\sdg11_3_1     

Save this notepad as a .env file within the cloned repository.

4. Userparams class 

## Usage 
?

## Input Data

This SDG indicator requires 4 distinct data types to be input: 

1. **A map of roads in the country of interest with classifications (eg. A-road, motorway).** Classifications are needed to establish all-season roads. The likely format for this data is .shp. 

2. **A geographic representation of population density.** Data on how many people live where is needed to establish distance of a population to an all-season road. Since the distance measured is 2km, data should be to (at least) 2km resolution, if not more detailed. The likely format of this data is .tiff (raster).  

3. **A classification of rural and urban areas.** This is needed to isolate the rural population. The likely format of this data is .csv.

4. **Administrative geography boundaries**. These boundaries provide a geographic reference to the rural-urban classification to compare spatially against population and roads, and thus needs match the geography used in the rural-urban classification. Eg, if the rural-urban classification uses Local Authority Districts (LADs), then LAD boundaries are required. The likely format of this data is .shp. 

Data used to calulate this SDG should be sampled from the same year.   

Since the United Kingdom is made up of four countries, each with their own methods of collecting and publishing data, total input data may amount to more than 4 sources. The SDG indicator should only be calulated using this code for countries where a full input dataset is available. 

[Further detail on requirements for SGG 9.1.1 as specified by the UN.](https://unstats.un.org/sdgs/metadata/files/Metadata-09-01-01.pdf) 

### Previously used data sources
    
Great Britain (roads): Ordnance Survey Open Roads. 
[https://www.ordnancesurvey.co.uk/products/os-mastermap-topography-layer](https://www.ordnancesurvey.co.uk/products/os-open-roads)
    
United Kingdom (population): WorldPop Hub Open Spatial Demographic Data and Research.
(https://hub.worldpop.org/)
        
England and Wales (rural-urban classification): Rural-Urban Classification, ONS Open Geography Portal.  
(https://geoportal.statistics.gov.uk/datasets/53360acabd1e4567bc4b8d35081b36ff/about)
    
England and Wales (statistical geography boundaries): Local-Authority District Boundaries, ONS Open Geography Portal. 
(https://geoportal.statistics.gov.uk/) 

## Methodology


       

## Outputs


### Considerations

**It may be possible to find a geographic representation of rural-urban classifications. In this instance, administrative boundaries won't be necessary. This code is however designed to be run with them as an input, so that step will need to be omitted.**

 
**GHS Settlement Grid**
 * Pesaresi, Martino; Freire, Sergio (2016):  GHS Settlement grid following the REGIO model 2014 in application to GHSL Landsat and CIESIN GPW v4-multitemporal (1975-1990-2000-2015). European Commission, Joint Research Centre (JRC) [Dataset] PID: http://data.europa.eu/89h/jrc-ghsl-ghs_smod_pop_globe_r2016a

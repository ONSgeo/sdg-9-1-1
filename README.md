## Introduction

The Sustainable Development Goals (SDGs) are part of the UN 2030 Agenda for Sustainable Development. The Office for National Statistics (ONS) reports the UK data for the SDG indicators on the [UK Sustainable Development Goals webpage](https://sdgdata.gov.uk/), contributing to progress towards a sustainable global future. 

Included in the 17 SDGs is Goal 9, which aims to ["Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation"](https://sdgs.un.org/goals/goal9). One indicator that supports this goal is **9.1.1: Proportion of the rural population who live within 2km of an all-season road**. This is commonly known as the Rural-Access Index (RAI). 

This code aims to provide an automated calculation of SDG indicator 9.1.1 for the timely reporting on progress towards Goal 9. The most recent reporting of this indicator by the UK covers the year [2011](https://sdgdata.gov.uk/9-1-1/).

### Set-up 
?
1. Clone this repository into the directory you'd like to work from. 
    
2. Create a .env file to set the directory from which inputs will be imported and results will be exported:

   Open the Notepad app and write ROOT_DIR= followed by the directory in which the input data is stored (and results we be exported to),  eg: 
    
    ROOT_DIR=C:\Users\username\scripts\sdg11_3_1     

Save this notepad as a .env file within the cloned repository.

4. Userparams class 

### Usage 

1. Clone this repository into the directory you'd like to work from. 

2. In the command-line interface, navigate to the root folder of the project and enter:
     
    pip install .
    
3. Create a .env file to set the user parameters. To do this, open Notepad and write `ROOT_DIR=` and the directory you'd like to work from,  eg: 
    
    ```ROOT_DIR=C:\Users\username\scripts\sdg15_1_1```     

Save this notepad as a `.env` file (by simply saving as `.env`) in the main directory you'd like to work from.

4. The **UserParams class (found in `user_params.py`) is where unique parameters are defined for the SDG indicator calculation.**
   
   It will make the assumption that input data will be located in the main directory within a folder named sdg_x_x_x_data, unless you specify a different `data_dir`, eg:
   
   if `self.data_dir: Optional[str] = None`:
   
   data will be stored in: `C:\Users\username\scripts\SDGs\sdg_x_x_x_data`

   else if `self.data_dir: Optional[str] = "C:\Users\username\somewhere_else"`:

   data will be stored in: `C:\Users\username\somewhere_else`

   This is also true for the output directory, where the default directory for output data will be: 'C:\Users\username\scripts\SDGs\sdg_x_x_x_output'

   For this SDG indicator the other user parameters are:
     - `raster_file_path`: The specific path to the raster population file for the single year
     - `ruc_file_path`: The specific path to the Rural Urban Classification file for the single year
     - `lad_file_path`: The specific path to the LAD shape file for the single year
     - `roads_file_path`: The specific path to the Roads shape file for the single year
     - `rural_class_col`: The column that contains the rural urban classifications
     - `road_class_col`: The column that contains the road type classifications
     - `road_classif_list`: The type of roads to filter out of the dataframe
     - `dissolve_col`: The column to dissolve the dataframes on
    
5. SDG9_1_1_Calculate can now be used!
      

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

## Output data

## Methodology

1. The Rural-Urban Classification (dataframe) is merged to geographic boundaries (geodataframe). This creates a spatial representation of rural areas. The merge is completed on a common column that is automatically determined based upon column similarity, so the input dataframes don't need to have a perfectly matched column. This subverts the need for the pre-processing of input data, such as when one dataset contains information covering Great Britain and the other only Wales and England. 

2. The newly created rural areas geodataframe is next overlayed onto the population raster. The resultant product is a geodataframe of the popualtion of rural areas; location, density and total popualtion. The overlay is completed as an intersection, thus discarding the urban population which is not relevant to the calculation of this indicator. 

3. Processing of the roads geodataframe is completed seperatley before merging to the rural popualtion geodataframe since it is typically very large in its raw format. Firstly, all-season roads are isolated by excluding non-all-season roads using a filter condition. The geometry of the roads are then buffered to 2000m to provide a catchment for areas > 2km from an all-season road. All-season roads in rural areas only are captured through an intersection overlay with the rural areas geodataframe, and the final buffered rural roads product is dissolved to geographic boundaries for simplification. 

4. The roads geodataframe and rural popualtion geodataframe are then spatially joined with the predicate "within" to produce a geodataframe of the population living within 2km of an all-season road.

5. The sum of the population living within 2km of an all season road is divided by the total rural population and multiplied by 100 to yield the percentage of the rural popualtion living within 2km of an all-season road.
     
**Calculations and methodology can be found within sdg_9_1_1.py in sdg_9_1_1.src folder.**

### Considerations

- It may be possible to find a geographic representation of rural-urban classifications. In this instance, administrative boundaries won't be necessary. This code is however designed to be run with them as an input, so that step will need to be omitted.
- This code uses LADs as default as the RUC was defined by LADs. This may not be the case in the future. Although the calculation will still hold up for any shapefile with an attribute table merginf with a csv, the nomenlature may become confusing.
- This method currently allows for the indicator to be calculated as a total for the areas covered by the input data. In order to calcualte this SDG at a higher granularity, eg per Local Authority district could be done but we haven't


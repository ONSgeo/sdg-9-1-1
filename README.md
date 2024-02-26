## Introduction

The Sustainable Development Goals (SDGs) are part of the UN 2030 Agenda for Sustainable Development. The Office for National Statistics (ONS) reports some of the UK data for the SDG indicators on the [UK Sustainable Development Goals webpage](https://sdgdata.gov.uk/), contributing to progress towards a sustainable global future. 

Included in the 17 SDGs is Goal 9, which aims to ["Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation"](https://sdgs.un.org/goals/goal9). One indicator that supports this goal is **9.1.1: Proportion of the rural population who live within 2km of an all-season road**. This is commonly known as the Rural-Access Index (RAI). 

This code aims to provide an automated calculation of SDG indicator 9.1.1 for the timely reporting on progress towards Goal 9. The most recent reporting of this indicator by the UK covers the year [2011](https://sdgdata.gov.uk/9-1-1/).

## Set-up

1. **Clone this repository** into the root directory you'd like to work from. 

2. **Install the SDG base class:** Open git BASH in the cloned repository and run the following two commands:

    ```git submodule init```

    ```git submodule update```

   The SDG base class handles methods common to all SDG indicator calculations and can be found in [this repository](https://github.com/ONSgeo/sdg_base).

4. **Create an environment variable** to set the address of the root directory. Using environment variables negates the need to enter personal information into the script. Open Notepad and write:

    `ROOT_DIR=C:\root\directory\address`
    
    Save this as the extension ".env" in the root directory. 

5. **Specify user parameters:** `user_params.py` requires user input:

- `root directory` will be taken from the environment variable.
- `data_dir` refers to the location of input data. If none is provided, it will assume the data is located within the root directory, in a folder named "sdg_x_x_x_data".
- `output_dir` refers to the location in which outputs should be stored. If none is provided, data will be output to the root directory as "sdg_x_x_x_output".
- **if only calculating for a single year**, set `single_year_test` to True.
- `year_start` expects the starting year for multiple exports. If calculating for a single year, this will be the date of that year.
- `year_end` expects the ending year for multiple year exports. If calculating for a single year, this will take None.
- `raster_file_path`: The specific path to the raster population file for the single year
- `ruc_file_path`: The specific path to the Rural Urban Classification file for the single year
- `lad_file_path`: The specific path to the LAD shape file for the single year
- `roads_file_path`: The specific path to the Roads shape file for the single year
- `rural_class_col`: The column that contains the rural urban classifications
- `road_class_col`: The column that contains the road type classifications
- `road_classif_list`: The type of roads to filter out of the dataframe
- `dissolve_col`: The column to dissolve the dataframes on
- `save_csv_file` will save results as .csv if set to True.


## Usage      


There is currently no usage notebook for SDG the calculation of SDG 9.1.1.


### Input Data

This SDG indicator requires 4 distinct data types to be input: 

1. **A map of classified roads in the country of interest (eg. A-road, motorway).** Classifications are needed to establish all-season roads. The assumed format for this data is .shp. 

2. **A geographic representation of population density.** Data on how many people live where is needed to establish distance of a population to an all-season road. Since the distance measured is 2km, data should be to (at least) 2km resolution. The assumed format of this data is .tiff (raster).  

3. **A classification of rural and urban areas.** This is needed to isolate the rural population. The assumed format of this data is .csv.

4. **Boundaries of administrative areas**. These boundaries provide a geographic reference to the rural-urban classification and thus needs match the granularity documented by the rural-urban classification: eg. if the rural-urban classification uses Local Authority Districts (LADs), then LAD boundaries are required. The assumed format of this data is .shp. 

Each data source used to calculate this SDG should be sampled from the same year(s).   

Since the United Kingdom is made up of four countries, each with their own methods of collecting and publishing data, total input data may amount to more than 2 sources. The SDG indicator should only be calculated for countries where a full input dataset is available. 

[Further detail on requirements for SGG 9.1.1 as specified by the UN.](https://unstats.un.org/sdgs/metadata/files/Metadata-09-01-01.pdf) 

### Methodology

1. The Rural-Urban Classification (dataframe) is merged to geographic boundaries (geo-dataframe). This creates a spatial representation of rural areas. The merge is completed on a common column that is automatically determined based upon column similarity, so the input dataframes don't need to have a perfectly matched column. This subverts the need for the pre-processing of input data, such as when one dataset contains information covering Great Britain and the other only Wales and England. 

2. The newly created rural areas geo-dataframe is next overlayed onto the population raster. The resultant product is a geo-dataframe of the population of rural areas; location, density and total population. The overlay is completed as an intersection, thus discarding the urban population which is not relevant to the calculation of this indicator. 

3. Processing of the roads geo-dataframe is completed separately before merging to the rural population geo-dataframe since it is typically very large in it's raw format. Firstly, all-season roads are isolated by excluding non-all-season roads using a filter condition. The geometry of the roads are then buffered to 2000m to provide a catchment for areas > 2km from an all-season road. All-season roads in rural areas only are captured through an intersection overlay with the rural areas geo-dataframe, and the final buffered rural roads product is dissolved to geographic boundaries for simplification. 

4. The roads geo-dataframe and rural population geo-dataframe are then spatially joined with the predicate "within" to produce a geo-dataframe of the population living within 2km of an all-season road.

5. The sum of the population living within 2km of an all-season road is divided by the total rural population and multiplied by 100 to yield the percentage of the rural population living within 2km of an all-season road.
     
Full programmatic calculation and methodology is found within `in sdg_9_1_1_src/sdg_9_1_1.py`.  

### Outputs

Currently available outputs include:

- Population and population within 2km of an all-season road for each specified rural area (.csv).


## Notes


### Previously used data sources
    
Great Britain (roads): Ordnance Survey Open Roads. 
[https://www.ordnancesurvey.co.uk/products/os-mastermap-topography-layer](https://www.ordnancesurvey.co.uk/products/os-open-roads)
    
United Kingdom (population): WorldPop Hub Open Spatial Demographic Data and Research.
(https://hub.worldpop.org/)
        
England and Wales (rural-urban classification): Rural-Urban Classification, ONS Open Geography Portal.  
(https://geoportal.statistics.gov.uk/datasets/53360acabd1e4567bc4b8d35081b36ff/about)
    
England and Wales (statistical geography boundaries): Local-Authority District Boundaries, ONS Open Geography Portal. 
(https://geoportal.statistics.gov.uk/) 


### Considerations

- The methodology of this indicator calculation is based upon assumed input data formats (see methodology). If better input data is found in an alternative format, methodology may need to be adjusted accordingly.
- It may be possible to find a geographic representation of rural-urban classifications. In this instance, administrative boundaries won't be necessary. This code is however designed to be run with them as an input, so that step will need to be omitted.
- This script refers to administrative boundaries as LADs by default in variables and functions since this is what we used in the initial calculation. The calculation will still hold up for any administrative boundary shapefile, although the nomenclature may become confusing.
- We chose to exclude roads classified by Ordnance Survey as "Not-Classified" and "Unknown" as being not all-season in our initial calculation. Since they are not explicitly defined as being all-season (or not), these definitions are open to some interpretation. 
- Please consult the [UN indicator requirements](https://unstats.un.org/sdgs/metadata/files/Metadata-09-01-01.pdf) for further considerations.

### Further work 

- The input data and methodology should be comprehensively compared against [UN specified requirements](https://unstats.un.org/sdgs/metadata/files/Metadata-09-01-01.pdf) when considering improvements.
- `sdg_9_1_1.py` currently has no notebook for ease of use. It would benefit from having one.
- This script currently allows for the indicator to be calculated as a total for the areas covered by the input data. It is possible (and probably useful) order to calculate this indicator at the highest level of granularity offered by the input data.
- The methodology of this calculator takes input data saved locally. The ability to directly stream input data, through an API or otherwise, is desirable but dependent on the data source. 

#### Authors

Ed Cuss (EdCussONS) & Lucy Astley-Jones (LucyAstleyJonesONS).


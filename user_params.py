import os
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class UserParams:
    def __init__(self) -> None:
        # the root directory to work from
        self.root_dir: Optional[str] = os.getenv("ROOT_DIR")

        # the directory where the data is located
        # if none the class will assume it is in: f'{self._root_dir}/{self._sdg_name}_data'
        # e.g.  'C:/Users/name/Scripts/SDGs/sdg_9_1_1_data'
        self.data_dir: Optional[str] = None

        # the directory where the output is saved
        # if none the class will assume it is in: f'{self._root_dir}/{self._sdg_name}_output'
        # e.g.  'C:/Users/name/Scripts/SDGs/sdg_9_1_1_output'
        self.output_dir: Optional[str] = None

        # the starting year for multiple year exports
        # the ONLY year for single year exports
        self.year_start: int = 2011

        # the ending year for multiple year exports
        self.year_end: int = 2022

        # if only testing a single year
        # Note this requires all the file paths below to be populated
        self.single_year_test: bool = True

        # The specific path to the raster population file for the single year
        self.raster_file_path: Optional[str] = (
            f"{self.root_dir}\\data\\sdg_9_1_1_data\\2020_gridded_popn_raster.tif"
        )

        # The specific path to the Rural Urban Classification file for the single year
        self.ruc_file_path: Optional[str] = (
            f"{self.root_dir}\\data\\sdg_9_1_1_data\\Rural_Urban_Classification_2011_lookup_tables_for_local_authority_areas.xlsx"
        )

        # The specific path to the LAD shape file for the single year
        self.lad_file_path: Optional[str] = (
            f"{self.root_dir}\\data\\sdg_9_1_1_data\\LAD-2011\\Local_Authority_Districts_December_2011_GB_BFE.shp"
        )

        # The specific path to the Roads shape file for the single year
        self.roads_file_path: Optional[str] = (
            f"{self.root_dir}\\data\\sdg_9_1_1_data\\2023_os_oproad\\2023_os_oproad.shp"
        )

        # The column that contains the rural urban classifications
        self.rural_class_col: str = "Rural Urban Classification 2011 (6 fold)"

        # The column that contains the road type classifications
        self.road_class_col: str = "road_class"

        # The type of roads to filter out of the dataframe
        self.road_classif_list: List[str] = ["Unknown", "Not Classified"]

        # The column to dissolve the dataframes on
        self.dissolve_col: str = "Local Authority District Area 2011 Code"

        # Option to save the resulting csv files
        self.save_csv_file: bool = True

    def print_params(self) -> None:
        for k, v in vars(self).items():
            print(f"{k} = {v}")

from typing import Dict, List, Optional, Tuple, Union

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio as rio

from src.sdg_9_1_1_src.sdg_base.base_src.sdg_base_src.sdg_base import SDGBase
from user_params import UserParams


class SDG9_1_1(SDGBase):
    """Defines input and output directories for data.

    Attributes (inherited)
    ----------
    root_dir
        The main directory in which data is stored.
    input_data_dir
        The main directory from which data is input.
    output_data_dir
        The main directory to which data is output.
    test_in_dir
        The main directory from which tests are drawn.
    test_out_dir
        The main directory to which tests are output.

    """

    def __init__(
        self,
        sdg_name: str,
        root_dir: Optional[str],
        data_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> None:
        """To retrieve input and save output data.

        Parameters
        ----------
        root_in_dir: str
            The main directory that the data is stored.
            For example: 'C:/Users/{user}/Scripts/geo_work/sdg_9_1_1/data'
        root_out_dir: Optional[str]
            This is for if the user wants to save the output elsewhere.
            If not the root out directory will be the same as the input directory.

        Returns
        -------
        None
        """

        self._sdg_name = "sdg_9_1_1"
        super().__init__(self._sdg_name, root_dir, data_dir, output_dir)

    def load_raster_data(
        self,
        raster_filepath: str,
    ) -> gpd.GeoDataFrame:
        with rio.Env():
            with rio.open(raster_filepath) as src:
                crs = src.crs

                # create 1D coordinate arrays (coordinates of the pixel center)
                xmin, ymax = np.around(src.xy(0.00, 0.00), 9)  # src.xy(0, 0)
                xmax, ymin = np.around(
                    src.xy(src.height - 1, src.width - 1), 9
                )  # src.xy(src.width-1, src.height-1)
                x = np.linspace(xmin, xmax, src.width)
                y = np.linspace(
                    ymax, ymin, src.height
                )  # max -> min so coords are top -> bottom

                # create 2D arrays
                xs, ys = np.meshgrid(x, y)
                zs = src.read(1)

                # Apply NoData mask
                mask = src.read_masks(1) > 0
                xs, ys, zs = xs[mask], ys[mask], zs[mask]

        data = {
            "X": pd.Series(xs.ravel()),
            "Y": pd.Series(ys.ravel()),
            "Z": pd.Series(zs.ravel()),
        }

        df = pd.DataFrame(data=data)
        geometry = gpd.points_from_xy(df.X, df.Y)
        gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

        # change crs to british national grid
        geometry = gpd.points_from_xy(df.X, df.Y)
        gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
        gdf.crs = "EPSG:27700"
        gdf.to_crs(epsg=27700)

        # remove the rows with 0 population
        gdf = gdf[gdf["Z"] > 0]
        return gdf

    def remove_rows_by_class(
        self,
        inp_gdf: Union[pd.DataFrame, gpd.GeoDataFrame],
        classification_col: str,
        value: str,
    ) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        cond = ~(inp_gdf[classification_col] == value)
        out_gdf = inp_gdf[cond]
        return out_gdf

    def remove_multiple_rows_by_class(
        self,
        gdf: Union[pd.DataFrame, gpd.GeoDataFrame],
        classification_col: str,
        remove_list: List[str],
    ) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        out_gdf = gdf.copy()
        for classif in remove_list:
            out_gdf = self.remove_rows_by_class(
                out_gdf, classification_col, classif
            )

        return out_gdf

    def check_similarity(self, arr1, arr2) -> float:
        set_1 = set(arr1)
        set_2 = set(arr2)
        similarity = len(set_1.intersection(set_2)) / len(set_1) * 100
        return similarity

    def get_max_similar_cols(
        self,
        inp_df1: Union[pd.DataFrame, gpd.GeoDataFrame],
        inp_df2: Union[pd.DataFrame, gpd.GeoDataFrame],
    ) -> Tuple[Dict[str, str], float]:
        """finds the columns with the max similarity

        Parameters
        ----------
        inp_df1 : Union[pd.DataFrame, gpd.GeoDataFrame]
            _description_
        inp_df2 : Union[pd.DataFrame, gpd.GeoDataFrame]
            _description_

        Returns
        -------
        Tuple[Dict[str, str], float]
            _description_
        """

        max_similarity = 0

        for col1 in inp_df1.columns:
            for col2 in inp_df2.columns:
                if inp_df1[col1].dtype == inp_df2[col2].dtype and (
                    col1 != "geometry" or col2 != "geometry"
                ):
                    array_dict = self.get_min_len_array(inp_df1, inp_df2)
                    similarity = self.check_similarity(
                        inp_df1[col1], inp_df2[col2]
                    )

                    if col1 in array_dict["min"].columns:
                        similarity = self.check_similarity(
                            array_dict["min"][col1], array_dict["max"][col2]
                        )
                    else:
                        similarity = self.check_similarity(
                            array_dict["min"][col2], array_dict["max"][col1]
                        )

                    if similarity > max_similarity:
                        max_similarity = similarity
                        similar_cols = {"df1": col1, "df2": col2}
        return similar_cols, max_similarity

    def attribute_merge_by_common(
        self,
        gdf: Union[gpd.GeoDataFrame, pd.DataFrame],
        df: Union[gpd.GeoDataFrame, pd.DataFrame],
        thresh=1,
    ) -> Optional[Union[gpd.GeoDataFrame, pd.DataFrame]]:

        similarity_cols, max_similarity = self.get_max_similar_cols(gdf, df)

        if max_similarity >= thresh:
            merged_gdf = gdf.merge(
                df,
                left_on=similarity_cols["df1"],
                right_on=similarity_cols["df2"],
            )
            return merged_gdf
        print("no match above threshold")
        return None

    def get_min_len_array(
        self, arr1, arr2
    ) -> Dict[str, Union[pd.DataFrame, gpd.GeoDataFrame]]:
        if len(arr1) < len(arr2):
            return {"min": arr1, "max": arr2}
        else:
            return {"min": arr2, "max": arr1}

    def remove_duplicate_cols(
        self, gdf: Union[pd.DataFrame, gpd.GeoDataFrame]
    ) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        drop_cols: List[str] = []

        for i, col1 in enumerate(gdf.columns):
            for col2 in gdf.columns[i + 1 :]:

                if col1 == col2:
                    continue
                if gdf[col1].equals(gdf[col2]):
                    drop_cols.append(col2)
        gdf = gdf.drop(columns=drop_cols)
        return gdf

    def calculate_sdg(
        self,
        raster_file_path: Optional[str],
        ruc_file_path: Optional[str],
        lad_file_path: Optional[str],
        roads_file_path: Optional[str],
        rural_class_col: str,
        road_class_col: str,
        road_classif_list: List[str],
        dissolve_col: str,
        year: int,
        save_csv_file: bool = False,
    ) -> bool:

        # Load files
        print("Loading data")
        raster_data = self.load_raster_data(raster_file_path)
        # ruc_data = self.load_data(ruc_file_path)
        ruc_data = pd.read_excel(
            ruc_file_path, sheet_name="LAD11_LAD13", header=2
        )
        lad_lookup_data = self.load_data(lad_file_path)
        os_roads_data = self.load_data(roads_file_path)

        # calculations
        print("Merging LAD and RUC data")
        ruc_output_areas = self.attribute_merge_by_common(
            lad_lookup_data, ruc_data
        )
        ruc_output_areas = ruc_output_areas
        rural_output_areas = self.remove_multiple_rows_by_class(
            ruc_output_areas,
            rural_class_col,
            [
                class_
                for class_ in ruc_output_areas[rural_class_col]
                if "rural" not in class_.lower()
            ],
        )
        print(rural_output_areas.head())

        print("Merging LAD and population data")
        rural_popn_lad = gpd.overlay(
            raster_data, rural_output_areas, how="intersection"
        )

        all_season_roads = self.remove_multiple_rows_by_class(
            os_roads_data, road_class_col, road_classif_list
        )
        print(all_season_roads.head())

        print("Buffering roads")
        all_season_roads = all_season_roads
        all_season_roads["geometry"] = all_season_roads["geometry"].buffer(
            2000
        )

        print("Overlaying buffered roads and RUC LADs")
        rural_road_catchment = gpd.overlay(
            all_season_roads, rural_output_areas, how="intersection"
        )
        rural_road_catchment_dis = rural_road_catchment.dissolve(
            by=dissolve_col
        )

        print("Joining LAD population with buffered roads")
        rural_popn_within = gpd.sjoin(
            rural_popn_lad, rural_road_catchment_dis, predicate="within"
        )
        res = (rural_popn_within["Z"].sum() / rural_popn_lad["Z"].sum()) * 100

        if save_csv_file:
            self.save_data(
                pd.DataFrame({"Year": year, "SDG_9_1_1": res}, index=[0]),
                f"sdg_9_1_1_{year}.csv",
            )

        return True


def run_sdg9_1_1(params: UserParams) -> None:

    gfr: SDG9_1_1 = SDG9_1_1(
        "", params.root_dir, params.data_dir, params.output_dir
    )

    if params.single_year_test and all(
        [
            params.raster_file_path,
            params.ruc_file_path,
            params.lad_file_path,
            params.roads_file_path,
            params.year_start,
        ]
    ):
        print(f"Running single year export for year: {params.year_start}")
        gfr.calculate_sdg(
            raster_file_path=params.raster_file_path,
            ruc_file_path=params.ruc_file_path,
            lad_file_path=params.lad_file_path,
            roads_file_path=params.roads_file_path,
            rural_class_col=params.rural_class_col,
            road_class_col=params.road_class_col,
            road_classif_list=params.road_classif_list,
            dissolve_col=params.dissolve_col,
            year=params.year_start,
            save_csv_file=params.save_csv_file,
        )

    else:
        print("Execution failed, please check necessary params:\n")
        params.print_params()

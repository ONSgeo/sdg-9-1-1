from typing import Optional
import unittest

import pandas as pd
import geopandas as gpd

from src.sdg_base_src import SDGBase
from ..base_user_params import UserParams


params: UserParams = UserParams()


class SDGConcrete(SDGBase):
    def __init__(self, sdg_name: str, root_dir: Optional[str], data_dir: Optional[str] = None, output_dir: Optional[str] = None, logger: bool = False) -> None:
        super().__init__(sdg_name, root_dir, data_dir, output_dir, logger)

    def calculate_sdg(self) -> bool:
        return True


class TestSDGBase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        print('Setting up class')
    

    def setUp(self) -> None:
        self._instance1: SDGConcrete = SDGConcrete('', params.root_dir)
        

    def test_get_input_data_dir(self) -> None:
        print('running test_get_input_data_dir')
        self.assertIsNotNone(self._instance1.get_input_data_dir())
        self.assertIsInstance(self._instance1.get_input_data_dir(), str)
    

    def test_set_input_data_dir(self) -> None:
        print('running test_set_input_data_dir')
        self._instance1.set_input_data_dir(params.root_dir)
        self.assertEqual(self._instance1.get_input_data_dir(), params.root_dir)


    def test_get_output_data_dir(self) -> None:
        print('running test_get_output_data_dir')
        self.assertIsNotNone(self._instance1.get_output_data_dir())
        self.assertIsInstance(self._instance1.get_output_data_dir(), str)


    def test_set_output_data_dir(self) -> None:
        print('running test_set_output_data_dir')
        self._instance1.set_output_data_dir(params.root_dir)
        self.assertEqual(self._instance1.get_output_data_dir(), params.root_dir)


    def test_get_read_function(self) -> None:
        print('running test_get_read_function')
        self.assertIs(self._instance1._get_read_function('csv'), pd.read_csv)
        self.assertIs(self._instance1._get_read_function('xlsx'), pd.read_excel)
        self.assertIs(self._instance1._get_read_function('shp'), gpd.read_file)
        
        

        

"""SDG 9.1.1"""

from src.sdg_9_1_1_src.sdg_base.src.sdg_base_src.sdg_base import SDGBase
from .sdg_9_1_1 import SDG9_1_1, run_sdg9_1_1

from typing import List

__all__: List[str] = [
    "SDGBase", 
    "SDG9_1_1", 
    "run_sdg9_1_1"
]
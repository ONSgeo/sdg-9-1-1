import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.sdg_9_1_1_src import SDG9_1_1
from user_params import UserParams

params: UserParams = UserParams()


def test_init():
    instance = SDG9_1_1("", params.root_dir)
    assert isinstance(instance, SDG9_1_1)


@given(
    st.lists(st.integers(), min_size=1, max_size=20),
    st.lists(st.integers(), min_size=1, max_size=20),
)
def test_check_similarity(arr1, arr2) -> None:
    instance = SDG9_1_1("", params.root_dir)

    result = instance.check_similarity(arr1, arr2)

    assert isinstance(result, float)
    assert 0.0 <= result <= 100.0
    assert (
        result == len(set(arr1).intersection(set(arr2))) / len(set(arr1)) * 100
    )


@pytest.mark.parametrize(
    "arr1, arr2, expected_res",
    [
        # ([], [], 100.0), TODO Catch zero division error
        ([0, 1, 2], [0, 1, 2], 100.0),
        ([0, 1, 2], [3, 4, 5], 0.0),
    ],
)
def test_check_similarity_defined_lists(arr1, arr2, expected_res) -> None:
    instance = SDG9_1_1("", params.root_dir)

    actual_res = instance.check_similarity(arr1, arr2)

    assert actual_res == expected_res


@given(
    st.lists(st.integers(), min_size=11),
    st.lists(st.integers(), min_size=1, max_size=10),
)
def test_get_min_len_array(arr1, arr2) -> None:
    instance = SDG9_1_1("", params.root_dir)

    result = instance.get_min_len_array(arr1, arr2)

    assert isinstance(result, dict)
    assert "min" in result
    assert "max" in result
    assert result["min"] == min(arr1, arr2, key=len)
    assert result["max"] == max(arr1, arr2, key=len)


@pytest.fixture
def create_remove_duplicate_cols_df():
    data = {"col1": [0, 1, 0, 1], "col2": [0, 1, 0, 1]}
    return pd.DataFrame().from_dict(data)


def test_filter_land_on_col(create_remove_duplicate_cols_df):
    instance = SDG9_1_1("", params.root_dir)

    result = instance.remove_duplicate_cols(create_remove_duplicate_cols_df)
    assert len(result.columns) == 1
    assert isinstance(result, pd.DataFrame)

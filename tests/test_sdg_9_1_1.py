import pytest 
from hypothesis import given, strategies as st

from src.sdg_9_1_1_src.sdg_9_1_1 import SDG9_1_1
from user_params import UserParams

params = UserParams()


@given(
    st.lists(st.integers(), min_size=1, max_size=20), 
    st.lists(st.integers(), min_size=1, max_size=20)
)
def test_check_similarity(arr1, arr2) -> None:
    instance = SDG9_1_1("", params.root_dir)

    result = instance.check_similarity(arr1, arr2)

    assert isinstance(result, float)
    assert 0.0 <= result <= 100.0
    assert result == len(set(arr1).intersection(set(arr2))) / len(set(arr1)) * 100


@pytest.mark.parameterize(
    "arr1, arr2, expected_res", 
    [
        ([], [], 100.0),
        ([0, 1, 2], [0, 1, 2], 100.0),
        ([0, 1, 2], [3, 4, 5], 0.0),
    ]
)
def test_check_similarity_defined_lists(arr1, arr2, expected_res) -> None:
    instance = SDG9_1_1("", params.root_dir)

    actual_res = instance.check_similarity(arr1, arr2)

    assert actual_res == expected_res


@given(
    st.lists(st.integers(), min_size=1),
    st.lists(st.integers(), min_size=1)
)
def test_get_min_len_array(arr1, arr2) -> None:
    instance = SDG9_1_1("", params.root_dir)

    result = instance.get_min_len_array(arr1, arr2)

    assert isinstance(result, dict)
    assert "min" in result
    assert "max" in result
    assert result["min"] == min(arr1, arr2, key=len)
    assert result["max"] == max(arr1, arr2, key=len)


if __name__ == '__main__':
    pytest.main()
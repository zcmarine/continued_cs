import pytest

from continued_cs.algorithms import build_subsets as bs


run_all_functions = pytest.mark.parametrize('fn', [
    (bs.build_subsets), (bs.build_subsets_recursive)
])


def compare_sets(a, b):
    for item in a:
        assert item in b
        b.remove(item)
    assert b == []


@run_all_functions
def test_build_subsets_empty(fn):
    input_ = set()
    actual = fn(input_)
    expected = [set()]
    compare_sets(actual, expected)


@run_all_functions
def test_build_subsets_one_element(fn):
    input_ = {3}
    actual = fn(input_)
    expected = [set(), {3}]
    compare_sets(actual, expected)


@run_all_functions
def test_build_subsets_two_elements(fn):
    input_ = {3, 5}
    actual = fn(input_)
    expected = [set(), {3}, {5}, {3, 5}]
    compare_sets(actual, expected)


@run_all_functions
def test_build_subsets_multiple_elements(fn):
    input_ = {3, 5, -1, 6}
    actual = fn(input_)
    expected = [set(),
                {3}, {5}, {-1}, {6},
                {3, 5}, {3, -1}, {3, 6}, {5, -1}, {5, 6}, {-1, 6},
                {3, 5, -1}, {3, 5, 6}, {5, -1, 6}, {3, -1, 6},
                {3, 5, -1, 6}]
    compare_sets(actual, expected)

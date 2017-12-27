import logging

import pytest

from continued_cs.algorithms import permute as p


logger = logging.getLogger('continued_cs.algorithms.permute')
logger.setLevel(logging.DEBUG)


run_all_functions = pytest.mark.parametrize('fn', [(p.permute), (p.permute_with_duplicates)])


def convert_list_of_lists(lol):
    ''' To compare our expected and output, we need our results as sets. This helper allows that '''
    return set(map(tuple, lol))


@run_all_functions
def test_one_element(fn):
    assert fn([3]) == [[3]]


@run_all_functions
def test_two_elements(fn):
    expected = convert_list_of_lists([[0, 1], [1, 0]])
    assert convert_list_of_lists(fn([0, 1])) == expected


@run_all_functions
def test_multiple_elements(fn):
    expected = convert_list_of_lists([
        [3, 4, 5],
        [3, 5, 4],
        [4, 3, 5],
        [4, 5, 3],
        [5, 3, 4],
        [5, 4, 3],
    ])
    assert convert_list_of_lists(fn([3, 4, 5])) == expected


def test_permute_with_duplicates_given_duplicates():
    expected = convert_list_of_lists([
        [3, 4, 5],
        [3, 5, 4],
        [4, 3, 5],
        [4, 5, 3],
        [5, 3, 4],
        [5, 4, 3],
    ])
    assert convert_list_of_lists(p.permute_with_duplicates([3, 4, 4, 5, 5])) == expected

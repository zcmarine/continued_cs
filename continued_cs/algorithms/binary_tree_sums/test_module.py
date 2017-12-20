import logging

import pytest

from continued_cs.algorithms.binary_tree_sums import partial_sums
from continued_cs.data_structures.binary_tree import create_binary_tree

logger = logging.getLogger('continued_cs.algorithms.binary_tree_sums')
logger.setLevel(logging.DEBUG)

# BIG_TREE (as used below):
#           4
#      -2      -7
#    3    8  2    9
#  6
BIG_TREE = create_binary_tree([4, -2, -7, 3, 8, 2, 9, 6])


def test_partial_sums_one_element_and_match():
    tree = create_binary_tree([3])
    _, counts = partial_sums(tree, 3)
    assert counts == 1


def test_partial_sums_one_element_no_match():
    tree = create_binary_tree([3])
    _, counts = partial_sums(tree, 4)
    assert counts == 0


def test_partial_sums_small_tree_multiple_matches():
    tree = create_binary_tree([1, 1, 2, 1])
    _, counts = partial_sums(tree, 3)
    assert counts == 2


@pytest.mark.parametrize('desired_val, expected_counts', [
    (2, 3),  # Matches: (4, -2), (-7, 9), (2)
    (9, 2),  # Matches: (3, 6), (9)
    (1, 1),  # Matches: (3, -2)
    (-33, 0),  # Matches: None
])
def test_partial_sums_big_tree_multiple_matches(desired_val, expected_counts):
    _, counts = partial_sums(BIG_TREE, desired_val)
    assert counts == expected_counts

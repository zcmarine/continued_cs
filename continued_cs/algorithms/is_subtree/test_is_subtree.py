import logging

import pytest

from continued_cs.data_structures.binary_tree import create_binary_tree
from continued_cs.algorithms import is_subtree

logger = logging.getLogger('continued_cs.algorithms.is_subtree')
logger.setLevel(logging.DEBUG)

# BIG_T1 (as used below):
#         4
#      2     7
#    3  8   5  9
#  6
BIG_T1 = create_binary_tree([4, 2, 7, 3, 8, 5, 9, 6])


def test_is_same_tree_one_element_true():
    node1 = create_binary_tree([2])
    node2 = create_binary_tree([2])
    assert is_subtree.is_same_tree(node1, node2)


def test_is_same_tree_one_element_false():
    node1 = create_binary_tree([1])
    node2 = create_binary_tree([2])
    assert not is_subtree.is_same_tree(node1, node2)


def test_is_same_tree_multiple_elements_true():
    node1 = create_binary_tree([2, 7, 3])
    node2 = create_binary_tree([2, 7, 3])
    assert is_subtree.is_same_tree(node1, node2)


def test_is_same_tree_multiple_elements_false():
    node1 = create_binary_tree([1, 6, 4])
    node2 = create_binary_tree([1, 5, 4])
    assert not is_subtree.is_same_tree(node1, node2)


def test_is_subtree_one_element():
    T1 = create_binary_tree([1])
    T2 = create_binary_tree([1])
    assert is_subtree.is_subtree(T1, T2)


@pytest.mark.parametrize('T2_array, expected', [
    ([7, 5, 9], True),
    ([3, 6], True),
    ([5], True),
    ([6, 9, 3], False),
    ([5, 6], False),
    ([12], False),
])
def test_is_subtree_multiple_elements(T2_array, expected):
    T2 = create_binary_tree(T2_array)
    assert is_subtree.is_subtree(BIG_T1, T2) is expected

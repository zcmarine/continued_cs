import pytest

from continued_cs.data_structures import binary_tree as bt


@pytest.mark.parametrize('idx, expected', [
    (0, 0), (1, 1), (2, 1), (3, 2), (6, 2), (7, 3)])
def test_get_level(idx, expected):
    assert bt.get_level(idx) == expected


@pytest.mark.parametrize('level, expected', [
    (0, 0), (1, 1), (2, 3), (3, 7)])
def test_get_min_idx(level, expected):
    assert bt.get_min_idx(level) == expected


@pytest.mark.parametrize('idx, expected', [
    (0, (1, 2)), (1, (3, 4)), (2, (5, 6)), (7, (15, 16))])
def test_get_childen(idx, expected):
    assert bt.get_children(idx) == expected


def test_binary_tree_one_element():
    actual = bt.create_binary_tree([0])
    assert actual.name == 0
    assert actual.left_child is None
    assert actual.right_child is None


def test_binary_tree_four_elements():
    actual = bt.create_binary_tree([3, 2, 7, 4])
    assert actual.name == 3
    assert actual.left_child.name == 2
    assert actual.right_child.name == 7
    assert actual.left_child.left_child.name == 4
    assert actual.left_child.right_child is None
    assert actual.right_child.left_child is None
    assert actual.right_child.right_child is None

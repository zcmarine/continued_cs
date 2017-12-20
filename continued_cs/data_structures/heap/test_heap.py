import logging

import pytest

from continued_cs.data_structures import heap


logging.getLogger('continued_cs.data_structures.heap').setLevel(logging.DEBUG)


@pytest.fixture
def minheap():
    return heap.MinHeap()


@pytest.mark.parametrize('idx, parent_idx', [
    (1, 0), (2, 0), (3, 1), (4, 1), (5, 2), (6, 2)
])
def test_get_parent(minheap, idx, parent_idx):
    assert minheap.get_parent(idx) == parent_idx


def test_get_parent_root(minheap):
    assert minheap.get_parent(0) is None


@pytest.mark.parametrize('idx, children_idxs', [
    (0, (1, 2)), (1, (3, 4)), (2, (5, 6)), (3, (7, 8))
])
def test_get_children(minheap, idx, children_idxs):
    minheap.h = list(range(10))
    assert minheap.get_children(idx) == children_idxs


@pytest.mark.parametrize('idx, children_idxs', [
    (4, (9, None)), (5, (None, None))
])
def test_get_children_dont_exist(minheap, idx, children_idxs):
    minheap.h = list(range(10))
    assert minheap.get_children(idx) == children_idxs


@pytest.mark.parametrize('h_given, idx1, idx2, h_expected', [
    ([1, 2], 0, 1, [2, 1]),
    ([3, 5, 7, 9], 3, 0, [9, 5, 7, 3]),
])
def test_swap(minheap, h_given, idx1, idx2, h_expected):
    minheap.h = h_given
    minheap.swap(idx1, idx2)
    assert minheap.h == h_expected


@pytest.mark.parametrize('h_given, h_expected', [
    ([1, 0], [0, 1]),
    ([5, 4, 3, 2, 1], [1, 5, 3, 2, 4]),
])
def test_percolate_up(minheap, h_given, h_expected):
    minheap.h = h_given
    minheap.percolate_up()
    assert minheap.h == h_expected


def test_push(minheap):
    assert minheap.h == []
    minheap.push(3)
    assert minheap.h == [3]
    minheap.push(2)
    assert minheap.h == [2, 3]
    minheap.push(5)
    assert minheap.h == [2, 3, 5]
    minheap.push(4)
    assert minheap.h == [2, 3, 5, 4]
    minheap.push(1)
    assert minheap.h == [1, 2, 5, 4, 3]


@pytest.mark.parametrize('h_given, parent_idx, expected_idx', [
    ([1, 0], 0, 1),
    ([1, 0], 1, None),
    ([5, 2, 3, 4, 5], 1, 3),
    ([5, 2, 3, 5, 4], 1, 4),
])
def test_get_idx_of_smaller_child(minheap, h_given, parent_idx, expected_idx):
    minheap.h = h_given
    smaller_child_idx = minheap.get_idx_of_smaller_child(parent_idx)
    assert smaller_child_idx == expected_idx


@pytest.mark.parametrize('h_given, h_expected', [
    ([1, 0], [0, 1]),
    ([5, 2, 3, 4], [2, 4, 3, 5]),
])
def test_percolate_down(minheap, h_given, h_expected):
    minheap.h = h_given
    minheap.percolate_down()
    assert minheap.h == h_expected


@pytest.mark.parametrize('h_given, h_expected, val_expected', [
    ([0, 1], [1], 0),
    ([8], [], 8),
    ([2, 2, 3, 4], [2, 4, 3], 2),
])
def test_pop(minheap, h_given, h_expected, val_expected):
    minheap.h = h_given
    assert val_expected == minheap.pop()
    assert minheap.h == h_expected


def test_pop_empty(minheap):
    with pytest.raises(Exception) as err:
        minheap.pop()
    assert err.match('Cannot pop from an empty heap')


def test_peek(minheap):
    assert minheap.peek() is None
    minheap.h = [1, 2]
    assert minheap.peek() == 1


def test_end_to_end(minheap):
    minheap.push(3)
    assert minheap.peek() == 3
    assert minheap.h == [3]

    assert minheap.pop() == 3
    assert minheap.h == []

    nums = (8, 2, 6, -7, 3, 1)
    for i in nums:
        minheap.push(i)
    assert minheap.peek() == -7
    assert minheap.h == [-7, 2, 1, 8, 3, 6]

    for i in sorted(nums):
        assert i == minheap.pop()

    assert minheap.h == []

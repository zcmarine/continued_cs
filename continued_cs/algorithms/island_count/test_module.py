import logging

import pytest

from continued_cs.algorithms import island_count

logger = logging.getLogger('continued_cs.algorithms.island_count')
logger.setLevel(logging.DEBUG)


def test_initialize_tracker_grid():
    tracker_grid = island_count.initialize_tracker_grid(nrows=3, ncols=5)
    assert len(tracker_grid) == 3
    assert len(tracker_grid[0]) == 5


def test_initialize_tracker_grid_rows_not_referencing_same_object():
    '''
    My previous initialization approach created one row and then n of them, but this just
    creates another reference to the same objects. This test is to assert I'm not still doing that

    For future reference to teach others, the old approach was:
        zeroed_col = [UNPROCESSED for col in range(ncols)]
        return [zeroed_col for row in range(nrows)]
    '''
    tracker_grid = island_count.initialize_tracker_grid(nrows=3, ncols=5)
    tracker_grid[0][0] = 'foo'
    assert tracker_grid[1][0] != 'foo'


@pytest.mark.parametrize('row, col, nrows, ncols, expected', [
    (0, 0, 1, 1, set()),
    (0, 0, 2, 2, set([(0, 1, island_count.FROM_NEIGHBOR), (1, 0, island_count.FROM_NEIGHBOR)])),
    (1, 1, 3, 3, set([(0, 1, island_count.FROM_NEIGHBOR), (2, 1, island_count.FROM_NEIGHBOR),
                      (1, 0, island_count.FROM_NEIGHBOR), (1, 2, island_count.FROM_NEIGHBOR)])),
])
def test_get_neighbors(row, col, nrows, ncols, expected):
    assert island_count.get_neighbors(row, col, nrows, ncols) == expected


def test_one_island():
    grid = [[1]]
    assert island_count.count_islands(grid) == 1


def test_one_island_non_square():
    grid = [[0, 0, 0],
            [0, 1, 0]]
    assert island_count.count_islands(grid) == 1


def test_one_multiblock_island_non_square():
    grid = [[0, 1, 0],
            [1, 1, 0]]
    assert island_count.count_islands(grid) == 1


def test_two_islands():
    grid = [[0, 1, 0],
            [1, 1, 0],
            [0, 0, 1]]
    assert island_count.count_islands(grid) == 2


def test_two_islands_non_square():
    grid = [[0, 1, 0, 0, 0],
            [1, 1, 0, 1, 0],
            [0, 0, 0, 1, 0]]
    assert island_count.count_islands(grid) == 2


def test_multiple_islands_bigger_example():
    grid = [[0, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 1, 1, 0, 1, 1]]
    assert island_count.count_islands(grid) == 5

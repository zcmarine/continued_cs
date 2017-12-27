import logging

import pytest

from continued_cs.algorithms import tower_of_hanoi as toh


logger = logging.getLogger('continued_cs.algorithms.tower_of_hanoi')
logger.setLevel(logging.DEBUG)


def test_initialize():
    t = toh.TowerOfHanoi(size=5)
    assert t.stacks[toh.START]._stack == [5, 4, 3, 2, 1]


@pytest.mark.parametrize('size', [(1), (2), (3), (8)])
def test_move_n_items(size):
    t = toh.TowerOfHanoi(size=size)
    assert t.stacks[toh.END]._stack == []

    t.move_all()

    assert t.stacks[toh.END]._stack == list(range(size, 0, -1))

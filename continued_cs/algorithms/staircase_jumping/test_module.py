import logging

import pytest

from continued_cs.algorithms.staircase_jumping import count_routes, count_routes_memoized

logger = logging.getLogger('continued_cs.algorithms.staircase_jumping')
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize('num_steps, expected', [
    # (3, 1)
    # (2, 1, 1), (2, 2)
    # (1, 1, 1, 1), (1, 2, 1), (1, 1, 2), (1, 3)
    (4, 7),
    # (3, 1, 1), (3, 2)
    # (2, 1, 1, 1), (2, 2, 1), (2, 1, 2), (2, 3)
    # (1, 3, 1), (1, 2, 1, 1), (1, 2, 2), (1, 1, 1, 1, 1), (1, 1, 2, 1), (1, 1, 1, 2), (1, 1, 3)
    (5, 13),
])
def test_count_routes(num_steps, expected):
    assert count_routes(num_steps) == expected


@pytest.mark.parametrize('num_steps, expected', [
    (4, 7),
    (5, 13),
])
def test_count_routes_memoized(num_steps, expected):
    assert count_routes_memoized(num_steps) == expected

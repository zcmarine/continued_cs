import logging

import pytest

from continued_cs.algorithms import egg_drop


logger = logging.getLogger('continued_cs.algorithms.egg_drop')
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize('n, k, expected', [
    (1, 1, 1), (1, 17, 17),
    (2, 5, 3), (2, 36, 8), (2, 100, 14),
])
def test_egg_drop(n, k, expected):
    assert egg_drop.egg_drop(n, k) == expected

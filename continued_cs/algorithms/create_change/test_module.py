import logging

import pytest

from continued_cs.algorithms import create_change as cc

logger = logging.getLogger('continued_cs.algorithms.create_change')
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize('cents, expected', [
    (1, 1),
    (5, 2),
    (9, 2),
    (10, 4),   # 10p, 1n5p, 2n, 1d
    (12, 4),   # 12p, 1n7p, 2n2p, 1d2p
    (25, 13),  # 1q  (+1)
               # 1d3n, 1d2n5p, 1d1n10p, 1d0n15p  (+4)
               # 2d1n, 2d5p (+2)
               # 0d5n, 0d4n5p, 0d3n10p, 0d2n15p, 0d1n20p (+5)
               # 25p (+1)
])
def test_count_change(cents, expected):
    ways = cc.create_change(cents)
    assert len(ways) == expected

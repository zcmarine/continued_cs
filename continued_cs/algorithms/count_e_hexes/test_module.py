import logging

import pytest

from continued_cs.algorithms import count_e_hexes as ceh


logger = logging.getLogger('continued_cs.algorithms.count_e_hexes')
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize('length, expected', [
    (1, 16), (3, 16**3),
])
def test_create_hex_colors(length, expected):
    assert len(ceh.create_hex_colors(length)) == expected


@pytest.mark.parametrize('length, expected', [
    (1, 1),
    (2, 16 + 15),  # 16 have an e in the 1st position and 16 has an e in the
                   # 2nd position; one is double-counted
])
def test_count_matching_items(length, expected):
    colors = ceh.create_hex_colors(length)
    assert ceh.count_matching_items(colors) == expected


@pytest.mark.parametrize('length', [
    (1), (2), (3),
])
def test_get_proportion(length):
    colors = ceh.create_hex_colors(length)
    cnt_from_counting = ceh.count_matching_items(colors)
    cnt_from_prob = ceh.get_proportion(length=length)
    assert cnt_from_counting == cnt_from_prob


@pytest.mark.slow
def test_get_proportion_length_6():
    '''
    This is why we did all this work; to make sure I'm doing my probability math correctly.

    Note that we're marking this test as slow and skipping it by default since we don't want the
    entire repo's test suite slowed down just for this one-time check. To run this check, just
    pass --slow when invoking pytest (i.e. `pytest --slow`).
    '''
    colors = ceh.create_hex_colors()
    cnt_from_counting = ceh.count_matching_items(colors)
    cnt_from_prob = ceh.get_proportion()
    assert cnt_from_counting == cnt_from_prob

import logging

import pytest

from continued_cs.algorithms import bit_manipulation as bm


logger = logging.getLogger('continued_cs.algorithms.bit_manipulation')
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize('b, num_bits, expected', [
    (0b1, 1, 0b0), (0b101, None, 0b10), (0b0101, 4, 0b1010), (0b11010, None, 0b101)
])
def test_negate(b, num_bits, expected):
    assert bm.negate(b, num_bits) == int(expected)


@pytest.mark.parametrize('i, expected', [(0, 1), (1, 0), (2, 0), (3, 1), (4, 0)])
def test_get_bit(i, expected):
    assert bm.get_bit(0b1001, i) == expected


@pytest.mark.parametrize('i, expected', [
    (0, 0b1001), (1, 0b1011), (2, 0b1101), (3, 0b1001), (4, 0b11001)])
def test_set_bit(i, expected):
    assert bm.set_bit(0b1001, i) == int(expected)


@pytest.mark.parametrize('i, expected', [
    (0, 0b1000), (1, 0b1001), (2, 0b1001), (3, 0b0001)])
def test_clear_bit(i, expected):
    assert bm.clear_bit(0b1001, i) == int(expected)


@pytest.mark.parametrize('i, val, expected', [
    (0, 0, 0b1000), (1, 0, 0b1001), (1, 1, 0b1011)])
def test_update_bit(i, val, expected):
    assert bm.update_bit(0b1001, i, val) == int(expected)


def test_insert_bin_exception():
    with pytest.raises(bm.SizeError) as err:
        bm.insert_bin(0b100, 0b010, 3, 2, b2_size=3)
    assert err.match('b2 does not fit into designated slot')


@pytest.mark.parametrize('b1, b2, i, j, b2_size, expected', [
    (0b100, 0b10, 1, 0, None, 0b110),
    (0b111, 0b10, 1, 0, None, 0b110),
    (0b10101, 0b10, 3, 2, None, 0b11001),
    (0b10101, 0b010, 4, 2, 3, 0b01001),
    (0b010101, 0b010, 4, 2, 3, 0b001001),
])
def test_insert_bin(b1, b2, i, j, b2_size, expected):
    assert bm.insert_bin(b1, b2, i, j, b2_size) == int(expected)


@pytest.mark.parametrize('num, expected', [
    (0b101, 3),
    (0b1011, 4),
    (0b01100111, 4),
    (0b11001, 3),
    (0b100, 2),
    (0b0, 1),
    (0b0000, 1),
    (0b1, 1),
    (0b11111, 5),
])
def test_longest_ones_with_flipped_bit(num, expected):
    assert bm.longest_ones_with_flipped_bit(num) == expected


@pytest.mark.parametrize('num, expected', [
    (0b1000, 0b100),
    (0b1011, 0b111),
    (0b10110, 0b10101),
    (0b1100, 0b1010),
    (0b10011110000011, 0b10011101110000),
])
def test_largest_smaller_num_same_1s(num, expected):
    assert bm.largest_smaller_num_same_1s(num) == expected


@pytest.mark.parametrize('bits, expected', [
    (1, 0b1),
    (3, 0b111),
    (5, 0b11111),
])
def test_ones(bits, expected):
    assert bm.ones(bits) == expected


@pytest.mark.parametrize('num, expected', [
    (0b101, 0b110),
    (0b10110, 0b11001),
    (0b1011, 0b1101),
    (0b100, 0b1000),
    (0b1100, 0b10001),
])
def test_smallest_larger_num_same_1s(num, expected):
    assert bm.smallest_larger_num_same_1s(num) == expected

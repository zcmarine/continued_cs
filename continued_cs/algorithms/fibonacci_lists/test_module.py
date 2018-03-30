import logging

import pytest

from continued_cs.algorithms import fibonacci_lists as fib


logger = logging.getLogger('continued_cs.algorithms.fibonacci_lists')
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize('num, expected', [
    (3, [1, 1, 2, 3]),
    (5, [1, 1, 2, 3, 5]),
    (8, [1, 1, 2, 3, 5, 8]),
])
def test_build_fibonacci_numbers(num, expected):
    assert fib.build_fibonacci_numbers(num) == expected


def test_build_fibonacci_numbers_not_a_fibonacci_number():
    with pytest.raises(ValueError) as err:
        fib.build_fibonacci_numbers(4)
    assert err.match('input num "4" is not a fibonacci number')


@pytest.mark.parametrize('num, expected', [
    (1, [
        [1]
    ]),


    (2, [
        [1, 1],
        [2],
    ]),


    (3, [
        [1, 1, 1],
        [2, 1],
        [3],
    ]),


    (5, [
        [1, 1, 1, 1, 1],
        [2, 1, 1, 1],
        [2, 2, 1],
        [3, 1, 1],
        [3, 2],
        [5],
    ]),


    (8, [
        [8],
        [5, 3],
        [5, 2, 1],
        [5, 1, 1, 1],
        [3, 3, 2],
        [3, 3, 1, 1],
        [3, 2, 2, 1],
        [3, 2, 1, 1, 1],
        [3, 1, 1, 1, 1, 1],
        [2, 2, 2, 2],
        [2, 2, 2, 1, 1],
        [2, 2, 1, 1, 1, 1],
        [2, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]),
])
def test_build_fibonacci_lists(num, expected):
    actual = fib.build_fibonacci_lists(num)
    assert sorted(actual) == sorted(expected)

import logging

import pytest

from continued_cs.algorithms import fibonacci_lists as fib


logger = logging.getLogger('continued_cs.algorithms.fibonacci_lists')
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize('input_, expected', [
    (3, [1, 1, 2, 3]),
    (4, [1, 1, 2, 3, 5]),
    (5, [1, 1, 2, 3, 5, 8]),
])
def test_generate_fibonacci_numbers(input_, expected):
    assert fib.generate_fibonacci_numbers(input_) == expected


def test_get_fibonacci_list_not_a_fibonacci_number():
    with pytest.raises(ValueError) as err:
        fib.get_fibonacci_list(4)
    assert err.match('num is not a fibonacci number')


def test_get_fibonacci_list_one():
    actual = fib.get_fibonacci_list(1)
    assert actual == [[1]]


def test_get_fibonacci_list_two():
    actual = fib.get_fibonacci_list(2)
    expected = [
        [1, 1],
        [2],
    ]
    assert actual == expected


def test_get_fibonacci_list_three():
    actual = fib.get_fibonacci_list(3)
    expected = [
        [1, 1, 1],
        [2, 1],
        [3],
    ]
    assert actual == expected


def test_get_fibonacci_list_four():
    actual = fib.get_fibonacci_list(5)
    expected = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 2],
        [2, 1, 1, 1],
        [2, 1, 2],
        [3, 1, 1],
        [3, 2],
        [5],
    ]
    assert actual == expected

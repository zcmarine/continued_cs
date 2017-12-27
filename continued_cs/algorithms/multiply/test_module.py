import pytest

from continued_cs.algorithms import multiply as m


run_all_functions = pytest.mark.parametrize('fn', [
    (m.multiply_with_while), (m.multiply_recursive), (m.multiply_logtime)
])


@run_all_functions
def test_multiply_by_zero(fn):
    assert fn(3, 0) == 0


@run_all_functions
def test_multiply_by_one(fn):
    assert fn(1, 7) == 7


@run_all_functions
def test_multiply_larger_odd_first(fn):
    assert fn(17, 24) == 408


@run_all_functions
def test_multiply_larger_odd_second(fn):
    assert fn(62, 43) == 2666

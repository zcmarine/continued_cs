import logging

import pytest

import incremental_median


logging.getLogger('heap').setLevel(logging.DEBUG)


@pytest.fixture(scope='function')
def minh():
    return incremental_median.Heap()


@pytest.fixture(scope='function')
def maxh():
    return incremental_median.Heap(is_minheap=False)


@pytest.fixture(scope='function')
def im():
    return incremental_median.IncrementalMedian()


class TestHeap:
    def test_init(self, minh):
        assert minh.h == []
        assert minh.sign == 1

    def test_minheap_pop(self, minh):
        minh._h = [1, 6, 3]
        assert minh.pop() == 1

    def test_minheap_push(self, minh):
        minh.push(6)
        minh.push(1)
        minh.push(3)
        assert minh._h == [1, 6, 3]

    def test_minheap_peek(self, minh):
        minh._h = [1, 6, 3]
        assert minh.peek() == 1
        assert minh._h == [1, 6, 3]

    def test_maxheap_pop(self, maxh):
        maxh._h = [-6, -1, -3]
        assert maxh.pop() == 6

    def test_maxheap_push(self, maxh):
        maxh.push(1)
        maxh.push(6)
        maxh.push(3)
        assert maxh._h == [-6, -1, -3]

    def test_maxheap_peek(self, maxh):
        maxh._h = [-8, -2, -5]
        assert maxh.peek() == 8


class TestIncrementalMedianFunctionality:
    def test_init(self, im, minh):
        assert im.minh.h == []
        assert im.maxh.h == []

    def test_get_median_even(self, im, minh, maxh):
        minh.push(7)
        maxh.push(4)
        im.minh = minh
        im.maxh = maxh
        assert im.get_median() == 0.5 * (4 + 7)

    def test_get_median_odd_and_empty(self, im, minh, maxh):
        minh.push(4)
        im.minh = minh
        assert im.get_median() == 4.0

    def test_get_median_odd_and_nonempty(self, im, minh, maxh):
        minh.push(5)
        minh.push(7)
        im.minh = minh
        maxh.push(1)
        im.maxh = maxh
        assert im.get_median() == 5.0

    def test_swap(self, im, minh, maxh):
        minh.push(1)
        minh.push(9)
        minh.push(7)
        im.minh = minh
        maxh.push(2)
        im.maxh = maxh
        im.swap()
        assert im.minh.h == [2, 9, 7]
        assert im.maxh.h == [1]

    def test_rebalance(self):
        pass

    def test_insert(self):
        pass


class TestEndToEnd:
    def test_one_insert(self, im):
        im.insert(3)
        assert im.get_median() == 3

    def test_two_inserts(self, im):
        im.insert(3)
        im.insert(5)
        assert im.get_median() == 4.0

    def test_two_inserts_one_negative(self, im):
        im.insert(3)
        im.insert(-3)
        assert im.get_median() == 0.0

    def test_two_inserts_both_negative(self, im):
        im.insert(-8)
        im.insert(-3)
        assert im.get_median() == -5.5

    def test_swapping_occurs(self, im):
        im.insert(11)
        im.insert(70)
        im.insert(10)
        assert im.get_median() == 11

    def test_multiple_swaps(self, im):
        for i in (10, 7, 4, 2, 4, 4, 1):
            im.insert(i)
        assert im.get_median() == 4

    @pytest.mark.parametrize('vals, expected', [
        ([6, 18, 42, 34, 35, 33, 47, 22, 90, 39, 98, 57, 7, 13, 94, 11, 56, 90, 15, 60], 37.0),
        ([17, 68, 37, 42, 88, 62, 91, 37, 68, 9, 26, 64, 82, 24, 85, 36, 51, 43, 68, 81], 56.5),
        ([31, 65, 44, 11, 44, 38, 24, 32, 3, 60, 91, 81, 39, 39, 15, 68, 57, 8, 94, 9], 39.0),
        ([57, 75, 22, 53, 52, 17, 71, 42, 43, 39, 18, 37, 31, 73, 95, 29, 27, 16, 89, 82], 42.5),
        ([19, 0, 66, 42, 0, 93, 14, 75, 18, 8, 5, 56, 49, 89, 74, 56, 70, 33, 12, 60], 45.5),
    ])
    def test_bigger_data_sets(self, im, vals, expected):
        ''' A variety of slightly larger data sets I tested against '''
        for val in vals:
            im.insert(val)
        assert im.get_median() == expected

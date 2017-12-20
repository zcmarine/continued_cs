import logging

from permute import permute


logger = logging.getLogger('permute')
logger.setLevel(logging.DEBUG)


def convert_list_of_lists(lol):
    ''' To compare our expected and output, we need our results as sets. This helper allows that '''
    return set(map(tuple, lol))


def test_one_element():
    assert permute([3]) == [[3]]


def test_two_elements():
    expected = convert_list_of_lists([[0, 1], [1, 0]])
    assert convert_list_of_lists(permute([0, 1])) == expected


def test_multiple_elements():
    expected = convert_list_of_lists([
        [3, 4, 5],
        [3, 5, 4],
        [4, 3, 5],
        [4, 5, 3],
        [5, 3, 4],
        [5, 4, 3],
    ])
    assert convert_list_of_lists(permute([3, 4, 5])) == expected

import logging

import pytest

from continued_cs.algorithms import reverse_linked_list as rll


logger = logging.getLogger('continued_cs.algorithms.reverse_linked_list')
logger.setLevel(logging.DEBUG)

SINGLE_ELEMENT_LIST = (7, )
IDENTICAL_ELEMENTS_LIST = (3, 3, 3)
MULTIPLE_ELEMENTS_LIST = (0, 1, 2, 3, 4, 5)


def generate_linked_list(l):
    ''' Pass a list to linked_list fixture for dynamically generated linked_list objects '''
    return pytest.mark.parametrize('linked_list', [l], indirect=True)


@pytest.fixture()
def linked_list(request):
    head = rll.Node(data=request.param[0])
    current = head
    for data in request.param[1:]:
        next_ = rll.Node(data=data)
        current.next = next_
        current = next_
    return head


@generate_linked_list(SINGLE_ELEMENT_LIST)
def test_reverse_linked_list_one_element(linked_list):
    reversed_ = rll.reverse_linked_list(linked_list)
    current = reversed_
    for data in SINGLE_ELEMENT_LIST:
        logger.debug(current.data)
        assert current.data == data
        current = current.next

    assert current is None


@generate_linked_list(IDENTICAL_ELEMENTS_LIST)
def test_reverse_linked_list_identical_elements(linked_list):
    reversed_ = rll.reverse_linked_list(linked_list)
    current = reversed_
    for data in IDENTICAL_ELEMENTS_LIST:
        logger.debug(current.data)
        assert current.data == data
        current = current.next

    assert current is None


@generate_linked_list(MULTIPLE_ELEMENTS_LIST)
def test_reverse_linked_list_multiple(linked_list):
    reversed_ = rll.reverse_linked_list(linked_list)
    current = reversed_
    for data in sorted(MULTIPLE_ELEMENTS_LIST, reverse=True):
        logger.debug(current.data)
        assert current.data == data
        current = current.next

    assert current is None


@generate_linked_list(SINGLE_ELEMENT_LIST)
def test_reverse_and_clone_linked_list_one_element(linked_list):
    reversed_ = rll.reverse_and_clone_linked_list(linked_list)
    current = reversed_
    for data in SINGLE_ELEMENT_LIST:
        logger.debug(current.data)
        assert current.data == data
        current = current.next

    assert current is None


@generate_linked_list(IDENTICAL_ELEMENTS_LIST)
def test_reverse_and_clone_linked_list_identical_elements(linked_list):
    reversed_ = rll.reverse_and_clone_linked_list(linked_list)
    current = reversed_
    for data in IDENTICAL_ELEMENTS_LIST:
        logger.debug(current.data)
        assert current.data == data
        current = current.next

    assert current is None


@generate_linked_list(MULTIPLE_ELEMENTS_LIST)
def test_reverse_and_clone_linked_list_multiple(linked_list):
    reversed_ = rll.reverse_and_clone_linked_list(linked_list)
    current = reversed_
    for data in sorted(MULTIPLE_ELEMENTS_LIST, reverse=True):
        logger.debug(current.data)
        assert current.data == data
        current = current.next

    assert current is None

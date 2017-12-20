import logging

import pytest

from continued_cs.algorithms import weave_linked_list as wll


logger = logging.getLogger('continued_cs.algorithms.weave_linked_list')
logger.setLevel(logging.DEBUG)


def generate_linked_list(l):
    ''' Pass a list to linked_list fixture for dynamically generated linked_list objects '''
    return pytest.mark.parametrize('linked_list', [l], indirect=True)


@pytest.fixture()
def linked_list(request):
    head = wll.Node(data=request.param[0])
    current = head
    for data in request.param[1:]:
        next_ = wll.Node(data=data)
        current.next = next_
        current = next_
    return head


@pytest.mark.parametrize('mutate', [True, False])
@generate_linked_list([0, 1, 2, 3, 4, 5])
def test_weave_even(linked_list, mutate):
    woven = wll.weave(linked_list, mutate)
    current = woven
    for data in [0, 3, 1, 4, 2, 5]:
        logger.debug(current.data)
        assert current.data == data
        current = current.next

    assert current is None


@pytest.mark.parametrize('mutate', [True, False])
@generate_linked_list([0, 1, 2, 3, 4])
def test_weave_odd(linked_list, mutate):
    woven = wll.weave(linked_list, mutate)
    current = woven
    for data in [0, 3, 1, 4, 2]:
        logger.debug(current.data)
        assert current.data == data
        current = current.next

    assert current is None


@pytest.mark.parametrize('mutate', [True, False])
@generate_linked_list([7, 3])
def test_weave_two_elements(linked_list, mutate):
    woven = wll.weave(linked_list, mutate)
    current = woven
    for data in [7, 3]:
        logger.debug(current.data)
        assert current.data == data
        current = current.next

    assert current is None


@pytest.mark.parametrize('mutate', [True, False])
@generate_linked_list([3])
def test_weave_one_element(linked_list, mutate):
    woven = wll.weave(linked_list, mutate)
    current = woven
    for data in [3]:
        logger.debug(current.data)
        assert current.data == data
        current = current.next

    assert current is None

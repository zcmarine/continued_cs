import logging

import pytest

import weave_linked_list as wll


logging.getLogger('weave_linked_list').setLevel(logging.DEBUG)


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


@generate_linked_list([0, 1, 2, 3, 4, 5])
def test_weave_even(linked_list):
    woven = wll.weave(linked_list)
    current = woven
    for data in [0, 3, 1, 4, 2, 5]:
        assert current.data == data
        current = current.next

    assert current is None


@generate_linked_list([0, 1, 2, 3, 4])
def test_weave_odd(linked_list):
    woven = wll.weave(linked_list)
    current = woven
    for data in [0, 3, 1, 4, 2]:
        assert current.data == data
        current = current.next

    assert current is None


@generate_linked_list([7, 3])
def test_weave_two_elements(linked_list):
    woven = wll.weave(linked_list)
    current = woven
    for data in [7, 3]:
        assert current.data == data
        current = current.next

    assert current is None


@generate_linked_list([3])
def test_weave_one_element(linked_list):
    woven = wll.weave(linked_list)
    current = woven
    for data in [3]:
        assert current.data == data
        current = current.next

    assert current is None

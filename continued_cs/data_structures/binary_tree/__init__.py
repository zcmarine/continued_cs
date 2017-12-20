'''
Create a binary tree assuming that the root is idx 0, its left child is idx 1, its right child is
idx 2, etc.
'''
import math


class Node(object):
    def __init__(self, name, parent, left_child=None, right_child=None):
        self.name = name
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child

    def __repr__(self):
        return '< Node {} >'.format(self.name)


def get_level(idx):
    return math.floor(math.log(idx + 1, 2))


def get_min_idx(level):
    return 2**level - 1


def get_children(root_idx):
    current_level = get_level(root_idx)
    min_level_idx = get_min_idx(current_level)
    offset = root_idx - min_level_idx
    left_child_idx = get_min_idx(current_level + 1) + 2*offset
    return (left_child_idx, left_child_idx + 1)


def create_binary_tree_helper(array, idx, parent):
    if idx > (len(array) - 1):
        return None

    left_child_idx, right_child_idx = get_children(idx)
    node = Node(name=array[idx], parent=parent)
    node.left_child = create_binary_tree_helper(array, idx=left_child_idx, parent=idx)
    node.right_child = create_binary_tree_helper(array, idx=right_child_idx, parent=idx)
    return node


def create_binary_tree(array):
    ''' Take a list and create a binary tree from it by assuming the 0th element is the root,
    the 1st and 2nd elements are the root's children, the 3rd and 4th elements are the 1st
    elements children, etc. In visual form:

                     0
              1             2
          3      4       5       6
        7  8   9  10   11  12  13  14

    In general, for each row the min_idx is (2^row) - 1 and the max_idx is (2^(row+1)) - 2

    Also, for a given node i, we find its children's indexes by calculating:
        1) how far is it from the min_idx for that row?  offset = i - (2^row) - 1
        2) offset * 2 will be how far off from the subsequent row's min_idx we start
        3) left_child will be min_idx for new row + offset * 2, then right_child is that +1

    for a given element i its children are i + 2^(row) and (i + 2^(row)) + 1

    '''
    return create_binary_tree_helper(array, idx=0, parent=None)

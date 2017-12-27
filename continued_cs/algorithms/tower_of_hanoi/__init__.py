import logging

from continued_cs.data_structures.stack import Stack


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


START = 0
END = 2
EXTRA = 1


class ItemTooLargeError(Exception):
    ''' Item is larger than top item on the stack it is being placed onto '''


class TowerOfHanoi(object):
    def __init__(self, size):
        self.size = size
        self.stacks = {
            START: Stack(),
            EXTRA: Stack(),
            END: Stack(),
        }

        self.initialize_start_stack()

    def initialize_start_stack(self):
        for i in range(self.size, 0, -1):
            self.stacks[START].push(i)

    def assert_valid_move(self, val, to):
        '''
        This should never be called, but it's better to be sure about that
        rather than trust our own coding skill...
        '''
        if not self.stacks[to].is_empty():
            curr_top = self.stacks[to].peek()
            if val > curr_top:
                err_msg = 'Item {} is larger than top value {} for tower {}'
                raise ItemTooLargeError(err_msg.format(val, curr_top, to))

    def move_top(self, from_, to):
        ''' Move an item from from stack to another '''
        val = self.stacks[from_].pop()
        self.assert_valid_move(val, to)
        logger.debug('Moving top item {} from {} to {}'.format(val, from_, to))
        self.stacks[to].push(val)

    @staticmethod
    def determine_tmp(a, b):
        # Which stack isn't being used yet?
        stacks = {START, END, EXTRA}
        diff = stacks.difference(set([a, b]))
        tmp = diff.pop()

        logger.debug('tmp = {}'.format(tmp))
        return tmp

    def move_n_items(self, n, from_, to):
        '''
        Move the top n items from one stack to another
        '''
        log_msg = 'Attempting to move {} items from {} to {}'
        logger.debug(log_msg.format(n, from_, to))

        tmp = self.determine_tmp(from_, to)

        if n == 1:
            # This is only called if there is only 1 element in the entire Tower Of Hanoi
            self.move_top(from_, to)
        elif n == 2:
            # This is the typical base case (i.e. the bottom of the recursion stack
            # so long as the Tower Of Hanoi has at least 2 elements total
            self.move_top(from_, tmp)
            self.move_top(from_, to)
            self.move_top(tmp, to)
        else:
            # Move n - 1 items to the tmp stack
            self.move_n_items(n - 1, from_, tmp)

            # Move the nth item to our destination
            self.move_top(from_, to)

            # Move the n - 1 items from our tmp location to our destination
            self.move_n_items(n - 1, tmp, to)

    def move_all(self):
        self.move_n_items(self.size, START, END)

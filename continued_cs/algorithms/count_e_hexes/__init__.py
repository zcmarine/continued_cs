from copy import deepcopy
import logging


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


HEX_CHARS = list('0123456789abcdef')


def create_hex_colors(length=6):
    '''
    A recursive approach to finding hex colors. A more efficient way of doing this is:

        hexes = [hex(i) for i in range(16**6)]

    With that said, this seemed like a simple way to practice recursion more, so I thought I'd give
    it a try.
    '''
    if length == 0:
        return ['#']
    else:
        colors = []
        bases = create_hex_colors(length-1)
        for i in HEX_CHARS:
            base_copy = deepcopy(bases)
            for base in base_copy:
                colors.append(base + i)

    return colors


def count_matching_items(colors):
    '''
    Determine matches by literally counting them. This is used as the check of our
    math from get_proportion().
    '''
    cnt = 0
    for item in colors:
        if 'e' in item:
            cnt += 1
    return cnt


def get_proportion(char_count=16, length=6):
    '''
    Mathematically derive the number of matching items.
    '''
    total = char_count**length

    has_e_proportion = 0
    for i in range(1, length+1):
        this_proportion = (1/char_count) * (((char_count-1)/char_count)**(i-1))
        print('i = {} / this_proportion = {}'.format(i, this_proportion))
        has_e_proportion += this_proportion

    return has_e_proportion * total

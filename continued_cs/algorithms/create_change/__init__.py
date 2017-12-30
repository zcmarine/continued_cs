import logging

from collections import namedtuple


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


Coin = namedtuple('Coin', ['name', 'value'])
denoms = [Coin('quarter', 25),
          Coin('dime', 10),
          Coin('nickel', 5),
          Coin('penny', 1),
          ]


class NegativeCentsException(Exception):
    ''' Negative cents were provided '''


def create_change(cents, idx=0, memo=None):
    '''
    Determine all possible ways we can create change for a given number of cents

    Uses dynamic programming to cache intermediate results; impact of the cache for
    create_change(3000): ~5s with cache vs. ~21-25s without cache
    '''
    # Initialize our memo for the top-level function call
    memo = memo or {k: dict() for k in range(len(denoms))}

    memoized_val = memo[idx].get(cents)
    if memoized_val:
        logger.debug('Using memoized value for idx={} cents={}'.format(idx, cents))
        return memoized_val

    this_coin = denoms[idx]
    logger.debug('create_change(cents={}, idx={})  # coin type = {}'.format(cents, idx, this_coin.name))

    if cents < 0:
        # This should never happen, but I'd prefer to be aware if I made a mistake
        raise NegativeCentsException('Negative cents were provided')

    if cents == 0:
        # Iterating through the previous denomination got us a match; we return an empty string
        # so that the calling function knows to add what it has as a separate successful match
        return ['']

    if this_coin.name == 'penny':
        logger.debug('Denom = penny; returning a success'.format(cents))
        return ['{} pennies'.format(cents)]

    ways = []
    this_coin_count = 0
    cents_remaining = cents
    while cents_remaining >= 0:
        sub_ways = create_change(cents_remaining, idx+1, memo)
        ways += ['{} {}s {}'.format(this_coin_count, this_coin.name, i) for i in sub_ways]

        cents_remaining -= this_coin.value
        this_coin_count += 1

    logger.debug('Setting memoized value for idx={} cents={}'.format(idx, cents))
    memo[idx][cents] = ways

    return ways

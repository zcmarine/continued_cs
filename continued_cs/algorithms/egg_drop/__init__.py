import logging
import sys


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def egg_drop(n, k, memo=None):
    '''
    ## Overview
    1. For each floor in [1, k], we will drop our egg. It will either:
        a. Break, in which case we try floors [1, k - 1] with n-1 eggs, i.e. k becomes floor - 1
        b. Not break, in which case we try floors [k + 1, k] with n eggs, i.e. k becomes (k - floor)
     2. We can't control if an egg breaks or not, so whichever of the above two cases results in
        more drops becomes our result for dropping at this floor
     3. However, we _can_ control which floor we will start dropping at, so we take the smallest
        value from all of these floors. That becomes the minimum number of drops we'd need to
        deterministically determine the lowest floor at which an egg will break

    Note that the parameters bottom_floor and top_floor are both inclusive, i.e. they will be
    checked
    '''
    # Initialize the memo for the first run
    memo = memo or [[None for i in range(k)] for j in range(n)]

    logger.debug('n={}, k={}'.format(n, k))
    if k == 0:
        logger.debug('0 floors being evaluated; returning 0')
        return 0

    if n == 1:
        # We have to drop at every floor
        return k

    logger.debug('n={}, k={}'.format(n, k))
    if memo[n-1][k-1] is not None:
        logger.debug('Using memo for n={}, k={}'.format(n, k))
        return memo[n-1][k-1]

    min_total_drops = sys.maxsize
    for floor in range(1, k+1):
        # Get maximum drops that may be required at this floor
        logger.debug('Invoking sub-helpers from n={}, k={}, floor={}'.format(n, k, floor))
        drops_if_broken = egg_drop(n-1, floor - 1, memo)
        drops_if_unbroken = egg_drop(n, k - floor, memo)
        required_drops = 1 + max(drops_if_broken, drops_if_unbroken)
        log_msg = 'Max drops {} for floor {} / n={} / k={}'
        logger.debug(log_msg.format(required_drops, floor, n, k))

        # We ultimately get to choose which floor to start dropping
        # at, so we can choose the minimum total number of drops
        min_total_drops = min(min_total_drops, required_drops)
    memo[n-1][k-1] = min_total_drops
    logger.debug('Setting memo for n={}, k={} to value {}'.format(n, k, min_total_drops))

    return min_total_drops

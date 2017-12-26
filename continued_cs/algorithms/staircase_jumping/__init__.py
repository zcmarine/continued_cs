import logging


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def count_routes(num_steps):
    if num_steps == 1:
        return 1
    elif num_steps == 2:
        return 2
    elif num_steps == 3:
        return 4

    # We'll be keeping track of the total for the 3 steps immediately above
    # the current one; initialize these values
    step_plus2_count = 1  # (1, )
    step_plus1_count = 2  # (1, 1), (2, )
    curr_step_count = 4   # (1, 1, 1), (2, 1), (1, 2), (3, )

    # Our current step is 3 down. We'll then keep moving down to the 0st step
    step = num_steps - 3
    while step >= 1:
        step -= 1

        # Shift all the step_plusX up one
        step_plus3_count = step_plus2_count
        step_plus2_count = step_plus1_count
        step_plus1_count = curr_step_count
        for var in ('step_plus1_count', 'step_plus2_count', 'step_plus3_count'):
            logger.debug('{}: {}'.format(var, eval(var)))

        # We can jump up 1, 2, or 3 steps, so our possibilities are
        # just the sum of the number of possibilities at those steps
        curr_step_count = step_plus1_count + step_plus2_count + step_plus3_count
        logger.debug('Count on step {}: {}'.format(step, curr_step_count))

    return curr_step_count


def count_routes_memoized(num_steps):
    '''
    A memoized solution to this problem. This works but is O(n) in its memory requirements. With
    that said, you'll end up with an integer overflow for even small values of n (e.g. n=1000), so
    the O(n) memory use is probably not a big deal, especially given that this approach is a bit
    simpler to reason about than the above solution which is O(1) in its memory use.
    '''
    memo = [None for _ in range(num_steps)]
    memo[num_steps - 1] = 1  # (1, )
    memo[num_steps - 2] = 2  # (1, 1), (2, )
    memo[num_steps - 3] = 4  # (1, 1, 1), (2, 1), (1, 2), (3, )

    return count_routes_memoized_helper(step=0, memo=memo)


def count_routes_memoized_helper(step, memo):
    if memo[step] is None:
        value = count_routes_memoized_helper(step + 1, memo) \
                + count_routes_memoized_helper(step + 2, memo) \
                + count_routes_memoized_helper(step + 3, memo)
        memo[step] = value
        logger.debug('Adding memo value for entry {}: {}'.format(step, value))
    return memo[step]

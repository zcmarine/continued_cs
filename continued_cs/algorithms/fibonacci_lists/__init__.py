import logging


logger = logging.getLogger(__name__)


def generate_fibonacci_numbers(n):
    """ Create the first n+1 fibonacci numbers (we do n+1 so we can
    assert that n is a fibonacci number) """
    if n <= 0:
        raise ValueError('n must be greater than 0')

    if n == 1:
        return [1]

    output = [1, 1]
    # We only decrement by 1 even though we already have
    # 2 numbers so that we end up with n+1 numbers
    n -= 1
    while n != 0:
        output.append(output[-1] + output[-2])
        n -= 1

    return output


def get_fibonacci_list(num):
    """ Given the input fibonacci num, generate all lists of fibonacci numbers that sum to this
    fibonacci number. For example, given the input 3 (which is a fibonacci number), the output
    should be:
        [
            [1, 1, 1],
            [2, 1],
            [3],
        ]
    """
    fibonacci_numbers = generate_fibonacci_numbers(num)
    if num not in fibonacci_numbers:
        raise ValueError('num is not a fibonacci number')

    ways_prev = [[1]]
    results = [[1]]

    # Start at the 3rd fibonacci number as we already have results for [1, 1]
    for fibnum in fibonacci_numbers[2:]:
        # We may have generated more fibonacci numbers than we
        # need so we need to stop processing
        if fibnum > num:
            break

        ways_two_prev = ways_prev
        ways_prev = results
        results = []

        logger.debug('fibnum: {}'.format(fibnum))
        logger.debug('ways_prev: {}'.format(ways_prev))
        logger.debug('ways_two_prev: {}\n'.format(ways_two_prev))

        # Do a cartesian product of the ways to create the two previous fibonacci numbers
        for prev_list in ways_prev:
            for two_prev_list in ways_two_prev:
                results.append(prev_list + two_prev_list)

        # We can create this fibonacci number from itself so add it to our list
        results.append([fibnum])

    return results

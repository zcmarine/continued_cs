import logging


logger = logging.getLogger(__name__)


def build_fibonacci_numbers(num):
    """ Create the fibonacci numbers up to and including a given fibonacci number """
    if num <= 0:
        raise ValueError('num must be greater than 0')

    if num == 1:
        return [1]

    output = [1, 1]
    while num > output[-1]:
        next_num = output[-1] + output[-2]
        output.append(next_num)

    if num != output[-1]:
        raise ValueError('input num "{}" is not a fibonacci number'.format(num))

    return output


def build_fibonacci_lists(num):
    """ Given the input fibonacci num, build all lists of fibonacci numbers that sum to this
    fibonacci number. For example, given the input 3 (which is a fibonacci number), the output
    should be:
        [
            [1, 1, 1],
            [2, 1],
            [3],
        ]
    """
    # We reverse the fibonacci numbers so we can peel them off from largest to smallest
    # We also make the fibonacci numbers a tuple so they are immutable just to be safe
    fibonacci_numbers = build_fibonacci_numbers(num)
    fibs = tuple(sorted(fibonacci_numbers, reverse=True))
    logger.debug('fibs: {}'.format(fibs))

    memo = {0: []}
    build_fibonacci_lists_helper(num, 0, [], fibs, memo)
    return memo[(num, 0)]


def build_fibonacci_lists_helper(num, idx, curr_list, fibs, memo):
    log_prefix = '{}({}, {}): '.format('  '*idx, num, idx)
    if (num, idx) in memo:
        results = memo[(num, idx)]
        logger.debug('{}Using memo entry {}'.format(log_prefix, results))

    curr_fib = fibs[idx]

    if num == 0:
        logger.debug('{}num = 0 for curr_fib = {}; returning curr_list = {}'.format(log_prefix,
                                                                                    curr_fib,
                                                                                    curr_list))
        results = [curr_list]
    elif curr_fib == 1:
        # We only have 1s left so pad the result with them
        results = [curr_list + [1]*num]
        logger.debug('{}curr_fib == 1 for num = {}; returning 1-padded list {}'.format(log_prefix,
                                                                                       num,
                                                                                       results))
    else:
        logger.debug('{}Calculating results'.format(log_prefix))
        div_count = num // curr_fib
        results = []
        for multiple in range(div_count+1):
            logger.debug('{}Recursing for multiple = {}'.format(log_prefix, multiple))
            subresults = build_fibonacci_lists_helper(
                num - multiple*curr_fib,
                idx+1,
                curr_list + multiple*[curr_fib],
                fibs,
                memo
            )
            results += subresults

    memo[(num, idx)] = results
    return results

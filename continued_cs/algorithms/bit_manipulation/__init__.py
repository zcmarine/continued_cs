import logging
import math


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class SizeError(Exception):
    ''' Second binary number does not fit into slot provided '''


def get_bit_length(num):
    return int(num).bit_length()


def negate(num, num_bits=None):
    '''
    Compute the negation of a number; if num_bits is None we will use the bit number's
    length to determine its size. num_bits can be provided if the number we're negating should be
    larger than the actual num provided, i.e. we're negating 0101 and care about that leading 0
    '''
    # In Python there is no negation operator (~ exists but does the binary number's
    # complement), but we can create this by creating an array of 1s and then XORing
    # our binary number with it
    num_bits = num_bits or get_bit_length(num)
    ones = (1 << (num_bits)) - 1
    return ones ^ num


def get_bit(num, i):
    # Create a mask at the ith bit, i.e. 00010000
    mask = 1 << i
    # AND this mask with our num, which will return either 00010000 or 0s
    applied = num & mask
    # Compare this result to 0; if it isn't 0 then the ith bit wasn't 0
    bit = applied != 0
    return int(bit)


def set_bit(num, i):
    # Create a mask at the ith bit, i.e. 00010000
    mask = 1 << i
    # OR this mask with our num, resulting in our num but with the ith bit set
    applied = num | mask
    return applied


def clear_bit(num, i):
    # Create a mask at the ith bit, i.e. 00010000
    mask = 1 << i
    # Invert the mask, i.e. 11101111. We need the mask size since i may not equal the size of num
    mask_size = get_bit_length(num)
    mask = negate(mask, num_bits=mask_size)
    # AND this mask and our num, returning num but with 0 for the ith bit
    return num & mask


def update_bit(num, i, val):
    # Clear the bit. Since we're dealing with bit manipulation, invoking a separate function
    # feels non-kosher (negate() is used above just because that's typically an available
    # bit operator
    mask = 1 << i
    mask_size = get_bit_length(num)
    mask = negate(mask, num_bits=mask_size)
    cleared = num & mask

    set_bit = val << i
    return cleared | set_bit


def insert_bin(b1, b2, i, j, b2_size=None):
    '''
    Insert a binary number b2 into binary number b1 starting at the ith index and ending at the
    jth index. Note that we must have i > j
    '''
    b2_size = b2_size or get_bit_length(b2)
    if b2_size != (i - j + 1):
        raise SizeError('b2 does not fit into designated slot')

    # Zero out the entries from i to j by. If i=3 and j=1:
    #    1) Create a binary number of all 1s, i.e. 1111111
    #    2) XOR that with a binary number of 1s from n to i, i.e. 1111111 ^ 0001111 = 1110000
    #    3) OR that with a binary number of 1s from j to 0, i.e. 1110000 OR 0000011 = 1110011
    ones = (1 << get_bit_length(b1)) - 1
    n_to_i_ones = (1 << (i + 1)) - 1
    j_to_0_ones = (1 << j) - 1
    mask = (ones ^ n_to_i_ones) | j_to_0_ones
    cleared = b1 & mask

    for var in ('n_to_i_ones', 'j_to_0_ones', 'mask', 'cleared'):
        logger.debug('{} entry: {}'.format(var, bin(eval(var))))

    # Insert the new number into our slot by ORing a shifted version of it
    shifted = b2 << j
    logger.debug('Shifted entry: {}'.format(bin(shifted)))
    result = cleared | shifted
    logger.debug('Result: {}'.format(bin(result)))
    return result


def longest_ones_with_flipped_bit(num):
    '''
    Take an int and compute the longest binary sequence of 1s we could get
    if we flipped one bit to a 1

    The basic approach is:
        0. Deal with the case where the number is zero (answer: 1) or the number is all 1s
           (answer: log(num + 1, 2))

    For everything else, we'll keep track of the size of the current and previous clump of 1s:
        1. Identify if the smallest bit is a 1 or 0.
        2. If the smallest bit is a 1, add +1 to our current clump of 1s
        3. Otherwise, we've hit a 0 so we'll see if (prev + curr + 1) is our new max,
           updating max if it is. In any case, it's time to start a new current clump,
           meaning we should set our existing current clump to be our previous one and
           set the new current clump to 0
        4. We now bit-shift our number one to the right, effectively making the second smallest bit
        the new smallest bit. We could do this with either num = (num >> 1) or by just
        floor-dividing by 2 (num //= 2)
        5. Repeat steps 1 through 4 until our number is zero, i.e. we've gone through all its bits
        6. After we've iterated through everything, we could end up with our last bit
           being a 1, so we need to see if (prev + curr + 1) exceeds our existing ma
    '''
    # Deal with the case where num is 0 or is a bunch of 1s
    if num == 0:
        return 1

    log = math.log(num+1, 2)
    if log == math.floor(log):
        return int(log)

    max_ = 1
    prev = 0
    curr = 0

    exp = 1
    while num != 0:
        bit = (num % 2**exp)
        num //= 2
        logger.debug('On bit idx {} (value: {})'.format(exp-1, bit))
        if bit == 1:
            curr += 1
        else:
            # Flip the zero between the prev and curr and count it
            this_size = prev + curr + 1
            if this_size > max_:
                max_ = this_size
                logger.debug('Updated max_ to: {}'.format(this_size))
            prev = curr
            curr = 0

    this_size = prev + curr + 1
    if this_size > max_:
        max_ = this_size
        logger.debug('Updated max_ to: {}'.format(this_size))
    return max_


def largest_smaller_num_same_1s(num):
    '''
    Given a number, return the largest number smaller than this but which has the same number of
    1s in its binary form.

    The basic idea is that we find the first 1 after we've found any 0s, then we switch that 1 with
    the largest 0 smaller than it. This is because we want to switch the smallest digits possible,
    but to change a 0 to a 1 we have to change a different 1 to a 0. To decrease the value, the
    bigger value must start as 1 and go to 0. Once we do that, we'll need to change a 0 to a 1 and
    the largest 0 we have would mean that the net different is the smallest. But wait! We also have
    to shift all 1s to the right of this point as far left as possible
    '''
    orig_num = num
    num_size = get_bit_length(num)
    count_ones = 0
    idx_zero = None
    idx_one = None
    idx = 0
    while num != 0:
        logger.debug('idx = {}'.format(idx))
        bit = (num % 2)
        num //= 2
        if bit == 1 and idx_zero is not None:
            idx_one = idx
            logger.debug('idx_one set to {}'.format(idx))
            break
        elif bit == 1:
            count_ones += 1
            logger.debug('count_ones increased to {}'.format(count_ones))
        else:
            idx_zero = idx
            logger.debug('idx_zero set to {}'.format(idx))

        idx += 1

    if idx_zero is None or idx_one is None:
        raise Exception('Unable to find smaller number that satisfies contraints')

    logger.debug('orig_num: {}'.format(bin(orig_num)))

    # Create mask to set our 0 bit to a 1
    to_one_mask = (1 << idx_zero)
    updated = (orig_num | to_one_mask)
    logger.debug('to_one_mask: {} / updated: {}'.format(bin(to_one_mask), bin(updated)))

    # Create mask to set our 1 bit to a 0
    to_zero_mask = (1 << idx_one)
    updated = (updated ^ to_zero_mask)
    logger.debug('to_zero_mask: {} / updated: {}'.format(bin(to_zero_mask), bin(updated)))

    # Create mask to clear all bits from idx_zero to bit 0, i.e. something like 111000000
    if num_size == idx_zero:
        clear_mask = ones(num_size + 1) ^ ones(idx_zero)
    else:
        clear_mask = ones(num_size) ^ ones(idx_zero)
    updated = (updated & clear_mask)
    logger.debug('clear_mask: {} / updated: {}'.format(bin(clear_mask), bin(updated)))

    # Create a mask to set the next count_ones bits to a 1
    ones_mask = ones(count_ones) << (idx_zero - count_ones)
    updated = (updated | ones_mask)
    logger.debug('ones_mask: {} / updated: {}'.format(bin(ones_mask), bin(updated)))

    return updated


def ones(bits):
    ''' Create a binary of ones that it `bits` bits long '''
    num = 0
    for bit in range(bits):
        num += 1 * 2**bit
    return num


def smallest_larger_num_same_1s(num):
    '''
    Given a number, return the smallest number larger than this but which has the same number of
    1s in its binary form.

    The basic idea is that we find the first 0 that is larger than a 1. We will then set that to a 1
    (in order to increase the number). At that point we will take all 1s smaller than this and shift
    them to the far right, less a single 1, i.e.:
        10110 - what we start with
        11110 - after we change the first 0 with a 1 behind it to a 1
        11011 - after we move to the right the 1s (less 1) that are smaller than the bit we flipped
    '''
    # find the smallest 0 after we've found a 1
    orig_num = num
    num_size = get_bit_length(num)
    idx_zero = None
    idx_one = None
    idx = 0
    count_ones = 0
    while num != 0:
        logger.debug('idx = {}'.format(idx))
        bit = (num % 2)
        num //= 2
        if bit == 0 and idx_one is not None:
            idx_zero = idx
            logger.debug('idx_zero set to {}'.format(idx))
            break

        if bit == 1:
            idx_one = idx
            logger.debug('idx_one set to {}'.format(idx))
            count_ones += 1
            logger.debug('count_ones increased to {}'.format(count_ones))

        idx += 1

    if idx_one is not None and idx_zero is None:
        # We have something like 0b100
        idx_zero = num_size

    # Create mask to set our 0 bit to a 1
    to_one_mask = (1 << idx_zero)
    updated = (orig_num | to_one_mask)
    logger.debug('to_one_mask: {} / updated: {}'.format(bin(to_one_mask), bin(updated)))

    # Create mask to clear all bits from idx_zero to bit 0, i.e. something like 111000000
    if num_size == idx_zero:
        clear_mask = ones(num_size + 1) ^ ones(idx_zero)
    else:
        clear_mask = ones(num_size) ^ ones(idx_zero)
    updated = (updated & clear_mask)
    logger.debug('clear_mask: {} / updated: {}'.format(bin(clear_mask), bin(updated)))

    # Create mask to recreate a bunch of 1s at the lowest bit indices
    ones_mask = ones(count_ones - 1)
    updated = (updated | ones_mask)
    logger.debug('ones_mask: {} / updated: {}'.format(bin(ones_mask), bin(updated)))

    return updated

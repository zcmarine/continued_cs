import logging


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def permute(array):
    '''
    To compute permutations of an array, lop off the last character and compute permutations on
    that. Once we have all of those, we just go through each of those subpermutations and insert
    that last character before and after each character in the subpermutation.
    '''
    logger.debug('array: {}'.format(array))
    if len(array) == 1:
        return [array]

    this_char = array[-1]
    logger.debug('array: {} // this_char: {}'.format(array, this_char))
    perm_subarray = permute(array[:-1])
    perm_array = []
    for one_subperm in perm_subarray:
        logger.debug('array: {} // one_subperm: {}'.format(array, one_subperm))
        for i in range(len(array)):
            one_perm = one_subperm.copy()
            one_perm.insert(i, this_char)
            perm_array.append(one_perm)

    return perm_array

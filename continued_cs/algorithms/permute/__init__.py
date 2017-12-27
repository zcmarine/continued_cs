from copy import deepcopy
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


def permute_with_duplicates(array):
    permutations, unique_eleemnts = permute_with_duplicates_helper(array)
    return permutations


def permute_with_duplicates_helper(array, processed=None):
    processed = processed or set()

    # Base Case
    if len(array) == 1:
        el = array[0]
        logger.debug('Adding item {} to processed list'.format(el))
        processed.add(el)
        return [[el]], processed

    arr = deepcopy(array)

    # Lop off the last item and compute all subpermutations excluding it
    this_char = arr.pop()
    logger.debug('array: {} // this_char: {}'.format(arr, this_char))
    perm_subarray, processed = permute_with_duplicates_helper(arr, processed)

    # If this_char has been processed, we don't need to do anything and can just return
    if this_char in processed:
        logger.debug('Character {} has already been processed; skipping'.format(this_char))
        return perm_subarray, processed

    # If we've gotten here, we haven't processed this character before. Add it to our processed list
    # and then compute all permutations with it (below)
    processed.add(this_char)
    logger.debug('Adding item {} to processed list'.format(this_char))
    logger.debug('processed: {}'.format(processed))

    # We now have all permutations excluding this_char. For each of those permutations, make a copy
    # of it and add this_char to the 0th index. Do the same for the 1st index, the 2nd, etc. This
    # means that if we had n subpermutations, each of length k, we will now have (k+1)n permutations
    # (the +1 is because we are adding this item at both the 0th and the -1st index).
    perm_array = []
    for one_subperm in perm_subarray:
        logger.debug('array: {} // one_subperm: {}'.format(array, one_subperm))
        for i in range(len(arr) + 1):
            one_perm = one_subperm.copy()
            one_perm.insert(i, this_char)
            perm_array.append(one_perm)

    return perm_array, processed

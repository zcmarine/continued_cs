import logging


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def partial_sums(node, desired_val):
    if node is None:
        return [], 0

    logger.debug('On node {}'.format(node.name))
    left_psums, left_counts = partial_sums(node.left_child, desired_val)
    logger.debug('left_psums: {}'.format(left_psums))
    right_psums, right_counts = partial_sums(node.right_child, desired_val)
    logger.debug('right_psums: {}'.format(right_psums))
    psums = left_psums + right_psums
    counts = left_counts + right_counts

    sums = [node.name]
    for psum in psums:
        sums.append(psum + node.name)
    logger.debug('sums for node {}: {}'.format(node.name, sums))

    for one_sum in sums:
        if one_sum == desired_val:
            counts += 1
            logger.debug('Count increased to {}'.format(counts))

    return sums, counts

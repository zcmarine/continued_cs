import logging

from continued_cs.data_structures.stack import Stack


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

UNPROCESSED = 0
PROCESSED = 1

FROM_INIT = 2
FROM_NEIGHBOR = 3


def initialize_tracker_grid(nrows, ncols):
    return [[UNPROCESSED for col in range(ncols)] for row in range(nrows)]


def get_neighbors(row, col, nrows, ncols):
    is_left_edge = col == 0
    is_right_edge = col == (ncols - 1)
    is_top_edge = row == 0
    is_bottom_edge = row == (nrows - 1)

    msg = 'Element ({}, {}) / is_left: {} / is_right: {} / is_top: {} / is_bottom: {}'
    logger.debug(msg.format(row, col, is_left_edge, is_right_edge, is_top_edge, is_bottom_edge))

    neighbors = set()
    if not is_left_edge:
        neighbors.add((row, col - 1, FROM_NEIGHBOR))
    if not is_right_edge:
        neighbors.add((row, col + 1, FROM_NEIGHBOR))
    if not is_top_edge:
        neighbors.add((row - 1, col, FROM_NEIGHBOR))
    if not is_bottom_edge:
        neighbors.add((row + 1, col, FROM_NEIGHBOR))

    return neighbors


def count_islands(grid):
    '''
    Given a grid of 1s and 0s, count the number of islands, where an island is all 1 elements that
    are touching one another. Diagonal elements are not considered touching.

    We do this by iterating through the grid and putting all elements on a stack. Then we start
    popping off that stack and, once we find an unprocessed piece of land we put all of its
    neighbors on the stack with an indication that these are adjoining an existing
    piece of land (so that they won't get marked as new land). If the source of our entry was that
    initial iteration that put things on the stack, then we also incremental our island count.

    Because the neighbors we added to the stack get processed before any of the other versions of
    that element that were put on in the initial iteration, those elements will be processed first,
    such that when they show up again later from that initial we skip them.
    '''
    if grid == []:
        return 0

    counts = 0
    nrows = len(grid)
    ncols = len(grid[0])

    tracker_grid = initialize_tracker_grid(nrows, ncols)

    # Create stack and put all elements on it, stating that these stack elements are being added
    # from this initialization period, in which case if the element is land we will count the land
    # as new
    stack = Stack()
    for row in range(nrows):
        for col in range(ncols):
            stack.push((row, col, FROM_INIT))

    while not stack.is_empty():
        row, col, source = stack.pop()
        is_processed = tracker_grid[row][col]
        if is_processed:
            logger.debug('Skipping element ({}, {}); already processed'.format(row, col))
            continue

        # Process this element. If it is land, put all unprocessed neighbors onto the stack as well
        # Also, if the source is FROM_INIT (and it is land), increment our count
        logger.debug('Processing element ({}, {})'.format(row, col))
        tracker_grid[row][col] = PROCESSED
        is_land = grid[row][col]
        if is_land:
            logger.debug('Element ({}, {}) is land'.format(row, col))
            if source == FROM_INIT:
                logger.debug('Element ({}, {}) is from init; incrementing count'.format(row, col))
                counts += 1

            for neighbor in get_neighbors(row, col, nrows, ncols):
                logger.debug('Adding neighbor {} of element ({}, {}) to stack'.format(neighbor, row, col))
                stack.push(neighbor)

    return counts

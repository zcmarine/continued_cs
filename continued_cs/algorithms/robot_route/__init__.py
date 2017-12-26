from copy import deepcopy
import logging

from continued_cs.data_structures.stack import Stack


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class NoRouteFoundException(Exception):
    '''Unable to find a route in the matrix provided'''


class Cell(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return 'Cell({}, {})'.format(self.row, self.col)


class KnownRoutes(object):
    def __init__(self, rows, cols):
        one_row = [[] for col in range(cols)]
        self.matrix = [deepcopy(one_row) for row in range(rows)]

    def get_route(self, cell):
        return self.matrix[cell.row][cell.col]

    def set_route(self, cell, base_cell=None):
        if not base_cell:
            base_route = []
        else:
            base_route = self.get_route(base_cell)

        self.matrix[cell.row][cell.col] = base_route + [(cell.row, cell.col)]


def get_adjoining_cells(cell, rows, cols):
    adj_cells = []
    if cell.row < (rows - 1):
        this_adj_cell = Cell(cell.row + 1, cell.col)
        adj_cells.append(this_adj_cell)
    if cell.col < (cols - 1):
        this_adj_cell = Cell(cell.row, cell.col + 1)
        adj_cells.append(this_adj_cell)

    return adj_cells


def find_route(matrix):
    '''
    Given a matrix of 0s (open cells) and 1s (blocked cells), find a route from the top left (0, 0)
    to the bottom right (r, c) subject to the constraint that you can only move down or right.
    '''
    rows = len(matrix)
    cols = len(matrix[0])
    if rows == 1 and cols == 1:
        return [(0, 0)]

    known_routes = KnownRoutes(rows, cols)
    cell = Cell(0, 0)
    known_routes.set_route(cell)

    stack = Stack()
    stack.push(cell)
    while not stack.is_empty():
        cell = stack.pop()
        logger.debug('Popping cell {}'.format(cell))
        for adj_cell in get_adjoining_cells(cell, rows, cols):
            # If this cell is blocked, continue on
            if matrix[adj_cell.row][adj_cell.col] == 1:
                logger.debug('Skipping blocked adjacent cell {}'.format(adj_cell))
                continue

            if not known_routes.get_route(adj_cell):
                known_routes.set_route(adj_cell, base_cell=cell)
                logger.debug('Adding route to cell {}'.format(adj_cell))
                logger.debug('Route is: {}'.format(known_routes.get_route(adj_cell)))

                stack.push(adj_cell)
                logger.debug('Pushing adjacent cell {} onto stack'.format(adj_cell))

            # Is it the bottom right cell?
            if adj_cell.row == (rows - 1) and adj_cell.col == (cols - 1):
                final_route = known_routes.get_route(adj_cell)
                logger.debug('Route to bottom right cell: {}'.format(final_route))
                return final_route

    raise NoRouteFoundException('Unable to find a route in the matrix provided')


def find_route_alt(matrix):
    '''
    Start at our destination and do a depth-first search back toward origin (0, 0). Along the way
    mark blockages. What makes this efficient is that we don't just label the cell that is a 1 but
    all "parents" that deterministically must end up at a 1 (i.e. all descendents of that route hit
    a 1 sometime). This means that the next time a DFS comes to that cell is will know not to keep
    looking

    Comparison to the above approach:
        + Fewer lines of code / more elegant
        + No need to store multiple potential routes so smaller memory footprint
        -/+ Max stack depth of r+c, though the other approach uses a Stack which could have even
            higher memory requirements
        - Harder to follow / more confusing because of the recursive calls
        - There's a subtle bug that can come up in this approach: if the `if at_start or...`
          creates variables for each of the find_route_alt_helper() recursive calls it makes then
          both of them will be executed to completion. If multiple routes between origin and the
          bottom right exist, then you will end up with all of those routes being appended together
          in a non-intuitive way. The subtlety of that bug is a big knock against this approach. To
          be more concrete, replace that if statement with the following and run the tests; the
          test_find_route_even_bigger() test will fail:

                a = find_route_alt_helper(matrix, row - 1, col, route, blockages)
                b = find_route_alt_helper(matrix, row, col - 1, route, blockages)
                if at_start or a or b:
    '''
    # Initialize everything for the top-level recursive call
    rows = len(matrix)
    cols = len(matrix[0])
    route = []
    blockages = []

    if rows == 1 and cols == 1:
        return [(0, 0)]

    if find_route_alt_helper(matrix, rows - 1, cols - 1, route, blockages):
        logger.debug('Route to bottom right cell: {}'.format(route))
        return route
    else:
        raise NoRouteFoundException('Unable to find a route in the matrix provided')


def find_route_alt_helper(matrix, row, col, route, blockages):
    if (row < 0) or (col < 0) or (matrix[row][col] == 1):
        return False

    cell = (row, col)
    logger.debug('On cell {}'.format(cell))
    if cell in blockages:
        logger.debug('Cell {} already in blockages; returning False'.format(cell))
        return False

    at_start = (row == 0 and col == 0)
    if at_start \
       or find_route_alt_helper(matrix, row - 1, col, route, blockages) \
       or find_route_alt_helper(matrix, row, col - 1, route, blockages):
        logger.debug('Cell {} can reach origin; adding to route'.format(cell))
        route.append(cell)
        return True
    else:
        logger.debug('Adding cell {} to blockages'.format(cell))
        blockages.append(cell)
        return False

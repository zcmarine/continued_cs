def multiply_with_while(x, y):
    result = 0
    while y >= 1:
        result += x
        y -= 1

    return result


def multiply_recursive(x, y):
    if y == 1:
        return x
    elif y == 0:
        return 0

    return x + multiply_recursive(x, y - 1)


def multiply_logtime(x, y):
    '''
    Do positive multiplication in O(logk) runtime where k is the value of the smaller of (x, y).
    This uses bit shifting to multiply and divide the two sides by 2 each time
    '''
    if (x == 0) or (y == 0):
        return 0

    smaller = x if x <= y else y
    bigger = x if x > y else y

    if smaller == 1:
        return bigger

    result = 0
    is_odd = (smaller & 1) != 0
    if is_odd:
        result += bigger

    # Use bit shifting to multiply one by 2 and divide the other by 2
    smaller >>= 1
    bigger <<= 1

    return result + multiply_logtime(smaller, bigger)

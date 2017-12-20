class Stack(object):
    def __init__(self):
        self._stack = []

    def is_empty(self):
        return len(self._stack) == 0

    def push(self, val):
        self._stack.append(val)

    def pop(self):
        return self._stack.pop()

    def peek(self):
        return self._stack[-1]

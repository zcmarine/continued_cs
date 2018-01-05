import logging

import pytest

from continued_cs.algorithms.regex_engine import is_match


logger = logging.getLogger('continued_cs.algorithms.regex_engine')
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize('text, pattern, expected', [
    ('aa', 'a', False),
    ('aa', 'aa', True),
    ('aaa', 'aa', False),
    ('aa', 'a*', True),
    ('aaaaa', 'a*', True),
    ('aaaab', 'a*b', True),
    ('aa', '.*', True),
    ('ab', '.*', True),
    ('aab', 'c*a*b', True),
])
def test_is_match(text, pattern, expected):
    assert is_match(text, pattern) is expected

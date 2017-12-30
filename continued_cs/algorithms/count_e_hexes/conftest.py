import pytest


def pytest_addoption(parser):
    parser.addoption('--slow', action='store_true', default=False, help='Also run slow tests')


def pytest_runtest_setup(item):
    '''
    Skip tests if they are marked as slow and --slow is not given. This and the above
    pytest_addoption function are directly taken from:

        http://blog.devork.be/2009/12/skipping-slow-test-by-default-in-pytest.html
    '''
    if getattr(item.obj, 'slow', None) and not item.config.getvalue('slow'):
        pytest.skip('slow tests not requested')

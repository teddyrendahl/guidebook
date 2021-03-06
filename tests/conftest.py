##############
#  Standard  #
##############
import logging

##############
#  External  #
##############
import pytest

##############
#   Module   #
##############

#Enable the logging level to be set from the command line
def pytest_addoption(parser):
    parser.addoption('--log', action='store', default='INFO',
                     help='Set the level of the log')

#Fixture to automatically instantiate logging setup
@pytest.fixture(scope='session', autouse=True)
def set_level(pytestconfig):
    #Read user input logging level
    log_level = getattr(logging, pytest.config.getoption('--log'), None)

    #Report invalid logging level
    if not isinstance(log_level, int):
        raise ValueError("Invalid log level : {}".format(log_level))

    #Create basic configuration
    logging.basicConfig(level=log_level, format='%(message)s')

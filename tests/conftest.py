##############
#  Standard  #
##############
import os.path
import logging

##############
#  External  #
##############
import pytest

##############
#   Module   #
##############

# Example Template Excel file
excel_template = os.path.join(os.path.dirname(__file__),'example.xlsx')

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

##############
#  Standard  #
##############
import os.path

##############
#  External  #
##############
import pytest

##############
#   Module   #
##############
from .conftest import excel_template
from guidebook import ExcelTemplate
from guidebook.parse import TemplatedTable 

def test_templated_table():
    #Grab table
    table =  TemplatedTable(excel_template, 3, 2, footer=27)
    #Check we got all the data and nothing more
    assert list(table.frame.index)   == ['Boulder A', 'Boulder B', 'Boulder C']
    assert list(table.frame.columns) == ['Comment'] 

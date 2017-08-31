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
from guidebook import ExcelTemplate
from guidebook.parse import TemplatedTable 

# Example Template Excel file
template = os.path.join(os.path.dirname(__file__),'example.xlsx')


def test_templated_table():
    #Grab table
    table =  TemplatedTable(template, 3, 2, footer=8)
    #Check we got all the data and nothing more
    assert list(table.frame.index)   == ['Boulder A', 'Boulder B', 'Boulder C']
    assert list(table.frame.columns) == ['Comment'] 
    
def test_parse_instantiate_area():
    #Parse Excel spreadsheet and create new area
    data = ExcelTemplate(template)
    area = data.instantiate_area()
    assert area.name == 'Area'
    assert len(area.boulders) == 3
    assert len(area.problems) == 6

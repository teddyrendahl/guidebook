##############
#  Standard  #
##############
import os
import os.path

##############
#  External  #
##############
import pytest

##############
#   Module   #
##############
from guidebook import Problem, Boulder, Area

@pytest.fixture(scope='module')
def area():
    #Instantiate problems
    problems = [Problem('Unknown', grade=2, stars=4,
                        comment='Test problem', number=3),
                Problem('Unknown', grade=2, stars=4,
                        comment='Test problem', number=3),
                Problem('Unknown', grade=2, stars=4,
                        comment='Test problem', number=3)]
    #Instantiate boulders
    boulders = [Boulder('Boulder 1', comment="Test boulder", problems=problems),
                Boulder('Boulder 2', comment="Test boulder", problems=problems),
                Boulder('Boulder 3', comment="Test boulder", problems=problems)]
    #Instantiate area
    return Area('Area', overview='Test area',
                directions='Test directions',
                boulders=boulders)


def test_area_rendering(area):
    tex = area.render()
    #Check area description
    assert tex.startswith(fake_area) 
    #Check each boulder is included
    assert all([boulder.render() in tex for boulder in area.boulders])


def test_area_subfile_creation(area):
    #Create subfile
    area.create_subfile(fname='test_area.tex', build_dir='./')
    #Assert file has been created with proper rendering
    with open('./test_area.tex', 'r') as f:
        assert area.render() == f.read()
    #Destroy file
    os.remove('test_area.tex')


fake_area = r"""\documentclass[main.tex]{subfiles} 
\begin{document}
\chapter*{Area}

Test area

Test directions"""

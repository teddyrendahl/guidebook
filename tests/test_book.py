##############
#  Standard  #
##############
import os
import os.path
import tempfile
from distutils.spawn import find_executable
##############
#  External  #
##############
import pytest

##############
#   Module   #
##############
from guidebook import Book, Problem, Boulder, Area
from guidebook.area import name_chapter

requires_latex = pytest.mark.skipif(find_executable('pdflatex') == None,
                                    reason= 'Test requires LaTex')

@pytest.fixture(scope='module')
def book():
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
    #Instantiate areas
    areas = [Area('Area 1', overview='Test area',
                  directions='Test directions',
                  boulders=boulders),
             Area('Area 2', overview='Test area',
                  directions='Test directions',
                  boulders=boulders),
             Area('Area 3', overview='Test area',
                  directions='Test directions',
                  boulders=boulders),
             Area('Area 4', overview='Test area',
                  directions='Test directions',
                  boulders=boulders)]
    #Instantiate book
    return Book(areas=areas)


def test_book_rendering(book):
    tex = book.render()
    #Check each area is included
    assert all([name_chapter(area.name) in tex for area in book.areas])


@requires_latex
def test_book_pdf_creation(book):
    with tempfile.TemporaryDirectory() as tmp:
        book.create_pdf('main.pdf', build_dir=tmp)
        assert os.path.exists(os.path.join(tmp, 'main.pdf'))


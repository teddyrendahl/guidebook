"""
Code for LaTex generation of entire areas
"""
##############
#  Standard  #
##############
import copy
import os.path
import logging

##############
#  External  #
##############
from latex.jinja2   import make_env
from jinja2.loaders import PackageLoader

##############
#   Module   #
##############

logger = logging.getLogger(__name__)

def name_chapter(area_name):
    """
    Create a .tex file name for an area
    
    Returns
    -------
    name : str
        Filename for area
    """
    return area_name.replace(' ','_').lower() + '.tex'


class Area(object):
    """
    Class to contain area information
    
    Parameters
    ----------
    name : str, optional
        Name of area

    overview : str, optional
        General overview of area

    directions : str, optional
        Directions to area

    boulders : list, optional
        List of :class:`.Boulder` objects
    """
    def __init__(self, name, overview=None, directions=None, boulders=None):
        self.name       = name
        self.overview   = overview
        self.directions = directions
        self.boulders   = boulders


    @property
    def problems(self):
        """
        All problems in the area
        """
        return [prob for bldr in self.boulders for prob in bldr.problems]


    def render(self, main_tex='main.tex'):
        """
        Create LaTex for area
        
        Parameters
        ---------
        main_tex : str, optional
            Relative location of main LaTex file. `main.tex` by default
        """
        #Create LaTex Jinja2 Environment
        env = make_env(loader=PackageLoader('guidebook'))
        tmpl = env.get_template('area.tex')
        #Grab all area information
        info = copy.deepcopy(vars(self))
        #Render all contained boulders and add main file location
        info.update({'boulders' : [bldr.render() for bldr in self.boulders],
                     'main_tex' : main_tex})
        return tmpl.render(info)


    def create_subfile(self, fname=None, build_dir=None, main_tex='main.tex'):
        """
        Create a LaTeX subfile for the area

        Parameters
        ----------
        fname : str, optional
            Name of file to create, otherwise one is generated based on the
            area name

        build_dir : str, optional
            Directory to place generated file
        
        main_tex : str, optional
            Relative location of main LaTex file. `main.tex` by default
        """
        #Generate name if not given one
        fname = fname or name_chapter(self.name)
        
        #Append build directory
        if build_dir:
            fname = os.path.join(build_dir, fname)

        #Render information into subfile
        logger.debug("Creating subfile for %s in %s...", self.name, fname)
        with open(fname, 'w+') as f:
            f.write(self.render(main_tex=main_tex))

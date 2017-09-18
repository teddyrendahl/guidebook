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
import numpy as np
import matplotlib.pyplot as plt
from latex.jinja2   import make_env
from jinja2.loaders import PackageLoader

##############
#   Module   #
##############
from .parse   import ExcelTemplate
from .problem import Problem, Boulder, color_for_grade
from .utils   import color_to_rgb

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

    def plot_problem_distribution(self):
        """
        Create a plot of the grade distribution

        Returns
        -------
        plot : matplotlib.Pyplot
            Bar Graph of problem distribution
        """
        max_grade   = 11
        star_cutoff = 4
        
        #Generate plot
        mpl_fig = plt.figure()
        ax = mpl_fig.add_subplot(111)

        #Sort by grade and stars
        histogram = np.histogram([prob.grade for prob in self.problems],
                                 bins=list(range(0, max_grade))+[16])[0]
        #Create chart
        ind = np.arange(0,max_grade)
        #Grab colors
        colors = [color_to_rgb[color_for_grade(i)] for i in ind]
        #Create bar graphs
        b1 = ax.bar(ind, histogram, color=colors, edgecolor='k')
        #Create labels
        ax.set_title('Grade Distribution for {}'.format(self.name))
        ax.set_ylabel('# of problems')
        #ax.set_yticks(np.arange(0, 18, 2))
        #Create X-labels
        xticks = ['V{}'.format(i) for i in ind]
        xticks[-1] += '+'
        ax.set_xticks(np.arange(len(xticks)))
        ax.set_xticklabels(xticks)
        #Create plot
        return mpl_fig

    def find_highlights(self, num=5):
        """
        Find the top rated problems of the area
        """
        #Grab top-rated problems
        highlights = sorted(self.problems, key = lambda x : x.stars)[:num]
        #Sort results by grade
        return sorted(hightlights, key = lambda x : x.grade)

    def render(self, main_tex='main.tex', build_dir=None):
        """
        Create LaTex for area
        
        Parameters
        ---------
        main_tex : str, optional
            Relative location of main LaTex file. `main.tex` by default

        build_dir : str, optional
            Directory to store permenant files

        Returns
        -------
        latex : str
            LaTeX representation of Area
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

    @classmethod
    def from_excel(cls, path):
        """
        Create an Area object from an Excel spreadsheet

        Parameters
        ----------
        path :str
            Path of ExcelTemplate

        Returns
        -------
        area : Area
        """
        #Load information into pandas
        tables = ExcelTemplate(path).find_tables()
        #Create problems
        problems = tables['Problems'].instantiate_objects(Problem)
        #Create boulders
        boulders = tables['Boulders'].instantiate_objects(Boulder)
        #Assign problems to boulders
        boulder_lookup = dict((bldr.name, bldr) for bldr in boulders)
        for problem in problems: 
            try:
                #Add problem to boulder by looking at boulder name
                boulder_lookup[problem.boulder].problems.append(problem)
            except KeyError as e:
                logger.error("Problem %s is on the %s boulder, but that "
                             "boulder does not exist",
                             problem.name, problem.boulder)
        #Create final area
        area = tables['Area Information'].instantiate_objects(Area)[0]
        #Assign boulders
        area.boulders = boulders
        logger.info("Successfully loaded area %s from Excel Workbook "
                    "%s, finding %s boulders with %s problems",
                    area.name, path, len(area.boulders),
                    len(area.problems))
        return area

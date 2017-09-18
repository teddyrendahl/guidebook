"""
Generation of individual boulder problem descriptions
"""
##############
#  Standard  #
##############
import copy
import logging

##############
#  External  #
##############
from latex.jinja2 import make_env

##############
#   Module   #
##############
from .templates import problem, boulder

logger = logging.getLogger(__name__)

def color_for_grade(grade):
    """
    Find the appropriate color for the grade
    
    Parameters
    ----------
    grade : int, None
        V-grade of the problem. If a proper color can not be found, `black` is
        returned

    Returns
    -------
    color : str
        Name of color
    """
    #Find templates
    for color, rng in Problem.grade_colors.items():
        if grade in rng:
            return color

    #Label non-graded climbs as projects
    logger.warning('Grade out of range, assuming the problem is a project')
    return 'black'

class Problem:
    """
    Class to represent an individual problem
    
    Attributes
    ----------
    grade_colors : dict
        Dictionary of color names to grade range mapping
    """
    #Group problems by grade
    grade_colors = {'ForestGreen' : range(0,3),
                    'blue'        : range(3,6),
                    'orange'      : range(6,9),
                    'red'         : range(9,16),
                    }

    #Link template
    template = problem

    def __init__(self, name, grade=None, stars=None, comment=None,
                 boulder=None, **kwargs):
        """
        Parameters
        ----------
        name : str
            Name of boulder

        grade : int
            V-Grade of problem

        stars : int
            Number of stars out of 5

        comment : str
            Short description of boulder

        boulder : str, optional
            Name of boulder
        """
        self.name    = name
        self.grade   = grade
        self.stars   = stars
        self.comment = comment
        self.boulder = boulder

    @property
    def color(self):
        """
        Proper color based on grade
        """
        return color_for_grade(self.grade)

    def render(self, num=0):
        """
        Render the boulder problem in LaTex
        
        Parameters
        ----------
        num : int
            Number of problem

        Returns
        -------
        template : str
            Templated string
        """
        #Create LaTex Jinja2 Environment
        env  = make_env()
        tmpl = env.from_string(self.template)
        #Grab all stored route information
        info = copy.deepcopy(vars(self))
        #Add problem number
        info['number'] = num
        #Add difficulty grouping
        info.update({'color' : self.color})
        return tmpl.render(info)

    def __repr__(self):
        return "<({} V{})>".format(self.name, self.grade)


class Boulder(object):
    """
    Class to represent a boulder with multiple problems
    
    Parameters
    ----------
    name : str
        Name of boulder

    comment : str, optional
        Directions or information about the boulder

    problems : iterable, optional
        Contained problems
    """
    template = boulder

    def __init__(self, name, comment=None, problems=None):
        self.name     = name
        self.comment  = comment
        self.problems = problems or []

    def render(self):
        """
        Render the boulder description and all problems into LaTex
        
        Parameters
        ----------
        num : int
            Number of problem

        Returns
        -------
        template : str
            Templated string
        """
        #Create LaTex Jinja2 Environment
        env  = make_env()
        tmpl = env.from_string(self.template)
        #Grab all stored boulder information
        info = copy.deepcopy(vars(self))
        #Render all contained problems
        info.update({'problems' : [prob.render(i+1)
                                   for i, prob in enumerate(self.problems)]})
        return tmpl.render(info)
    
    def __repr__(self):
        return "<({}, {} problems)>".format(self.name, len(self.problems))

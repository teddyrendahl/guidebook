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

class Problem:
    """
    Class to represent an individual problem
    
    Attributes
    ----------
    grade_colors : dict
        Dictionary of color names to grade range mapping
    """
    #Group problems by grade
    grade_colors = {'beginner'   : range(0,3),
                    'moderate'   : range(3,6),
                    'hard'       : range(6,9),
                    'difficult'  : range(9,16),
                    }

    #Link template
    template = problem

    def __init__(self, name, grade=None,
                 stars=None, comment=None,
                 number=None):
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

        number : int
            Problem number on boulder
        """
        self.name    = name
        self.grade   = grade
        self.stars   = stars
        self.comment = comment
        self.number  = number


    @property
    def color(self):
        """
        Proper color based on grade
        """
        #Find templates
        for color, rng in self.grade_colors.items():
            if self.grade in rng:
                return color

        #Label non-graded climbs as projects
        logger.warning('Grade out of range, assuming %s is a '
                       'project', self.name)
        return 'project'


    def render(self):
        """
        Render the boulder problem in LaTex
        """
        #Create LaTex Jinja2 Environment
        env  = make_env()
        tmpl = env.from_string(self.template)
        #Grab all stored route information
        info = copy.deepcopy(vars(self))
        #Add difficulty grouping
        info.update({'color' : self.color})
        return tmpl.render(info)



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
        self.problems = problems


    def render(self):
        """
        Render the boulder description and all problems into LaTex
        """
        #Create LaTex Jinja2 Environment
        env  = make_env()
        tmpl = env.from_string(self.template)
        #Grab all stored boulder information
        info = copy.deepcopy(vars(self))
        #Render all contained problems
        info.update({'problems' : [prob.render() for prob in self.problems]})
        return tmpl.render(info)

"""
Utility functions for guidebook creation
"""
##############
#  Standard  #
##############

##############
#  External  #
##############
from latex.jinja2 import make_env

##############
#   Module   #
##############
from .templates import table

color_to_rgb = {'ForestGreen' : (34/255,139/255,34/255),
                'blue'        : (0, 0, 1),
                'orange'      : (1, 165/255, 0),
                'red'         : (1, 0, 0),}

def create_table(problems, color):
    """
    Create a table of problems

    Parameters
    ----------
    problems : list
        List of `Problem` objects

    Returns
    -------
    latex : str
        LaTex representation of table
    """
    #Create LaTex template
    env  = make_env()
    tmpl = env.from_string(table)
    #Populate with tab
    return templ.render(problems=problems, color=color)

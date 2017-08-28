"""
Generation of complete LaTex Guide 
"""
##############
#  Standard  #
##############
import os.path
import logging
from collections import Iterable

##############
#  External  #
##############
from latex import LatexBuildError, build_pdf
from latex.jinja2 import make_env
from latex.errors import parse_log
from jinja2.loaders import PackageLoader

##############
#   Module   #
##############
from .area import name_chapter

class Book(object):
    """
    Class to combine all chapters into final book PDF
    """
    def __init__(self, areas=None):
        self.areas= areas


    def render(self):
        """
        Create main LaTex file for guidebook
        """
        #Create LaTex Jinja2 Environment
        env = make_env(loader=PackageLoader('guidebook'))
        tmpl = env.get_template('main.tex')
        #Grab all area information
        info = {'areas' : [name_chapter(area.name) for area in self.areas]}
        return tmpl.render(info)  


    def create_pdf(self, fname=None, build_dir=None, include_subfiles=True):
        """
        Create a PDF of the guidebook
        
        Parameters
        ----------
        fname : str, optional
            Name of file to create, otherwise `main.pdf` is used

        build_dir : str, optional
            Directory to build LaTex files

        include_subfiles : bool or Iterable
            Rebuild all, None or some of the chapter subfiles.
        """
        #Append build directory
        build_dir = build_dir or './'
        fname     = fname or 'main.pdf'
        fname = os.path.join(build_dir, fname)
        
        #Save main tex file
        tex_name = os.path.splitext(fname)[0] + '.tex'
        with open(tex_name, 'w+') as f:
            f.write(self.render())

        #Gather specified subfiles
        if isinstance(include_subfiles, Iterable):
            subfiles = include_subfiles
        #All subfiles
        elif include_subfiles:
            subfiles = self.areas
        #No subfiles
        else:
            subfiles = []

        #Build selected subfiles
        for sub in subfiles:
            sub.create_subfile(build_dir=build_dir,
                               main_tex=fname)
        #Create the PDF
        pdf = build_pdf(open(tex_name, 'r').read(), texinputs=[build_dir])
        pdf.save_to(fname)

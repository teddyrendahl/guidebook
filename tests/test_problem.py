##############
#  External  #
##############
import pytest

##############
#   Module   #
##############
from guidebook import Problem, Boulder

def test_problem_rendering():
    #Instantiate problem
    problem = Problem('Unknown', grade=2, stars=4,
                      comment='Test problem', number=3)
    #Render tex
    tex = problem.render(3)
    assert tex == fake_problem
    
    #Instantiate project
    problem = Problem('Unknown', grade=None, stars=4,
                      comment='Test problem', number=3)
    #Render tex
    tex = problem.render(3)
    assert tex == fake_project

def test_boulder_rendering():
    #Instantiate problems
    problems = [Problem('Unknown', grade=2, stars=4,
                        comment='Test problem'),
                Problem('Unknown', grade=2, stars=4,
                        comment='Test problem'),
                Problem('Unknown', grade=2, stars=4,
                        comment='Test problem')]
    #Instantiate boulders
    boulder = Boulder('Unknown', comment='Test boulder', problems=problems)
    #Render tex
    tex = boulder.render()
    #Check the boulder description
    assert tex.startswith(fake_boulder)
    #Check each problem is included
    assert all([problem.render(i+1) in tex
                for i,problem in enumerate(problems)])
    
fake_boulder = r"""
% ---------------------------------------------------
% Unknown
% ---------------------------------------------------
\section{Unknown}
Test boulder"""


fake_problem=r"""
% -------------------
%  Unknown  
% -------------------
\beginner{3}\hspace{1.5mm}\textbf{{\large Unknown}}
V2
$ \color{red}
    \bigstar
    \bigstar
    \bigstar
    \bigstar
$
\hfill $\square$
\vspace{1.5mm}
\newline
Test problem
\newline\newline"""


fake_project=r"""
% -------------------
%  Unknown  
% -------------------
\project{3}\hspace{1.5mm}\textbf{{\large Unknown}}
$ \color{red}
    \bigstar
    \bigstar
    \bigstar
    \bigstar
$
\hfill $\square$
\vspace{1.5mm}
\newline
Test problem
\newline\newline"""

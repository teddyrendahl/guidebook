##############
#  External  #
##############
import pytest

##############
#   Module   #
##############
from guidebook import Problem

def test_problem_rendering():
    #Instantiate problem
    problem = Problem('Unknown', grade=2, stars=4,
                      comment='Test problem', number=3)
    #Render tex
    tex = problem.render()
    assert tex == r"""
% -------------------
%  Unknown  
% -------------------
\beginner{3}\hspace{1.5mm}\textbf{{\large Unknown}} V2
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

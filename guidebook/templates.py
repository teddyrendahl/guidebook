"""
Basic LaTex templates for formatting guidebook objects 
"""
###################################
# Template for Individual Problem #
###################################
problem=r"""
% -------------------
%  \VAR{name}  
% -------------------
\\VAR{color}{\VAR{number}}\hspace{1.5mm}\textbf{{\large \VAR{name}}}
%- if color != 'project'
V\VAR{grade}
%- endif
$ \color{red}
%- for star in range(0, stars)
    \bigstar
%- endfor
$
\hfill $\square$
\vspace{1.5mm}
\newline
\VAR{comment}
\newline\newline"""

###################################
# Template for Individual Boulder #
###################################
boulder=r"""
% ---------------------------------------------------
% \VAR{name}
% ---------------------------------------------------
\section{\VAR{name}}
%- if comment
\VAR{comment}
%- endif
%- for problem in problems
    \VAR{problem}
%- endfor"""

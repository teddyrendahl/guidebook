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
\\VAR{color}{\VAR{number}}\hspace{1.5mm}\textbf{{\large \VAR{name}}} V\VAR{grade}
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

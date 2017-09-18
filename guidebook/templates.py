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
\circlednumber{\VAR{number}}{\VAR{color}}\hspace{1.5mm}\textbf{{\large \VAR{name}}}
%- if color != 'black'
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

##############################
# Template for Rounded Table #
##############################
table=r"""
\begin{rndtable}{l r r}}
    \multicolumn{4}{c}{\cellcolor{color}\color{white} Highlights} \\ \hline
%- for problem in problems
    \VAR{problem.name} & \VAR{problem.grade} & %-for star in range(0, problem.stars)\bigstar%-endfor \\
%- endfor
    \end{rndtable}
"""

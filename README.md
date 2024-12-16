# AAAI25-CDCL-OCAC
Code, dataset and appendix for the AAAI25 paper


## Instructions of Reproducibility

We also provide the source code for the implementation. The license is the same as the original CVC5 because it is a derived tool on CVC5. You should add a tag:  ``(set-logic OMT\_QF\_NRA)'' to enable the optimization mode. (Because CVC5 does not have an OMT parser and remove all optimization codes after 1.0.8). One can generate benchmarks and build solvers using the command:
\begin{equation}
    \text{./prepare.sh} \nonumber
\end{equation}
One can run our solver parallel using the command:
\begin{equation}
    \text{./parallel\_our\_solver.sh \texttt{cdcl\_ocac}} \nonumber
\end{equation}
One can run other solvers \texttt{solver} using command:
\begin{equation}
    \text{./parallel\_other\_solver.sh \texttt{solver}} \nonumber
\end{equation}
% One can generate corresponding quantified formula from an SMT file \texttt{file} to the given directory \texttt{output\_dir} using command:
% \begin{equation}
%     \text{python qtransformer.py \texttt{file} \texttt{output\_dir}} \nonumber
% \end{equation}


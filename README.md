# Supplementary of AAAI25 paper
Code, dataset, and appendix for the AAAI25 paper: A Complete Algorithm for Optimization Modulo Nonlinear Real Arithmetic.


## Instructions of Reproducibility

We also provide the source code and dataset in the ``Supplementary`` directory. The license is the same as the original CVC5 because it is a derived tool on CVC5. You should add a tag:  ``(set-logic OMT\_QF\_NRA)'' to enable the optimization mode. (Because CVC5 does not have an OMT parser at version 1.0.8). One can generate benchmarks and build solvers using the command:
```
    ./prepare.sh
```
One can run our solver parallelly using the command:
```
    ./parallel_our_solver.sh cdcl_ocac
```
One can run other solvers **s** (e.g. Z3, OptiMathSAT, ...) using the command:
```
    ./parallel_other_solver.sh s
```

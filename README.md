# AAAI25-CDCL-OCAC
Code, dataset and appendix for the AAAI25 paper


## Instructions of Reproducibility

We also provide the source code for the implementation. The license is the same as the original CVC5 because it is a derived tool on CVC5. You should add a tag:  ``(set-logic OMT\_QF\_NRA)'' to enable the optimization mode. (Because CVC5 does not have an OMT parser and remove all optimization codes after 1.0.8). One can generate benchmarks and build solvers using the command:
```
    ./prepare.sh
```
One can run our solver parallel using the command:
```
    ./parallel_our_solver.sh cdcl_ocac
```
One can run other solvers **s** (e.g. Z3, OptiMathSAT, ...) using the command:
```
    ./parallel_other_solver.sh s
```

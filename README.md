# Supplementary Materials for AAAI-25 Paper

**A Complete Algorithm for Optimization Modulo Nonlinear Real Arithmetic**

## Code Repository

The source code is publicly available at:
🔗 [https://github.com/fuqi-jia/cdcl\_ocac](https://github.com/fuqi-jia/cdcl_ocac)

## Reproducibility Instructions

We provide the complete source code, dataset, and appendix in the `Supplementary` directory. The project is based on CVC5 and inherits its license, as it is a derived work.

> **Note:** To enable optimization mode, you must add the SMT-LIB tag:
> `(set-logic OMT_QF_NRA)`
> This is necessary because CVC5 (version 1.0.8) does not support OMT parsing by default.

### Setup

To prepare the environment, generate benchmarks, and build the solvers, run:

```bash
./prepare.sh
```

### Running the Solvers

* To run **our solver** in parallel:

```bash
./parallel_our_solver.sh cdcl_ocac
```

* To run **other solvers** (e.g., Z3, OptiMathSAT, etc.) in parallel:

```bash
./parallel_other_solver.sh <solver_name>
```

Replace `<solver_name>` with the name of the desired solver.

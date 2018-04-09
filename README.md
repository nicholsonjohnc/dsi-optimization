# DSI Optimization
Optimization Lecture and Assignment - Galvanize Data Science Immersive (DSI)

## Step 1 - Install Pyomo and Solvers
[Pyomo](http://www.pyomo.org/) is a Python-based, open-source optimization modeling language developed at Sandia National Laboratories.

Optimization or Algebraic Modeling Languages (AMLs) allow us to formulate optimization problems in terms of our problem/business logic.  They provide a common interface to optimization solvers.  Also, they abstract away some of the complexities of formulating optimization problems (e.g. computing gradients of the objective and constraint functions with respect to the decision variables).

Pyomo is unique relative to other AMLs in that it is implemented in code.  Most AMLs (e.g. AMPL, GAMS, RASON, etc.) read in text or json files and output optimization problems.  Pyomo allows us to create optimization problems directly in Python and export, if necessary, our problem to other formats.

Pyomo supports a wide range of optimization problem types:

* Linear programming
* Quadratic programming
* Nonlinear programming
* Mixed-integer linear programming
* Mixed-integer quadratic programming
* Mixed-integer nonlinear programming
* Stochastic programming
* Generalized disjunctive programming
* Differential algebraic equations
* Bilevel programming
* Mathematical programs with equilibrium constraints

You will, however, need to find/install appropriate underlying solvers in order to actually solve these problem types. We will stick with open-source solvers today. If you ever can't find/install an appropriate solver or want to give a commercial-solver a try you may want to send your problem to the [NEOS server](https://neos-server.org/neos/).

OK, let's get back to it. Install Pyomo with the following terminal command:

```
conda install -c conda-forge pyomo
```

Enter ```y``` when prompted to proceed.

Enter ```pyomo --version``` to confirm Pyomo was installed.

Now let's install a solver. [GLPK](https://www.gnu.org/software/glpk/) or GNU Linear Programming Kit solves large-scale Linear Programming (LP) and Mixed Integer Programming (MIP) problems.

```
conda install -c conda-forge glpk
```

## Step 2 - Complete Newsvendor Class

Finish implementing the objective_stochastic, model_stochastic, and solve_stochastic methods in the Newsvendor class.






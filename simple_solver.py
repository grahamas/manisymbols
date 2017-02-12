#!/usr/bin/env python3

# Graham Smith

# Methods to implement the simplest equation method of solving differential
# equations where you have a "complex" equation you want to solve, and a
# "simple" equation whose solution you know and whose solution you suspect to be
# fundamentally similar to that of the "complex" equation (e.g. u_x = u - u^2 is
# a simple equation with the same fundamental tanh solution as the KdV equation.


def simple_derive(complex_eqn, simple_eqn):
    """
    Use the simplest equation method to derive complex_eqn from simple_eqn
    """
    pass


def simple_tree(simple_eqn, depth):
    """
    Make a tree of derivations from simple_eqn, of a particular differentaion
    depth. Probably requires some notion of "effective" differentiation depth,
    with respect to the function of interest, rather than simply the function
    used in the expression.
    """
    pass

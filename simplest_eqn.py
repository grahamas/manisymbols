#!/usr/bin/env python3

# An implementation of the simplest equation method

# Assuming one function, one variable

d_objects = {}


class Expression(object):

    def __init__(self, factor=1, power=1, derivative=0):
        self.factor = factor
        self.power = power
        self.derivative = derivative


class OpExpression(Expression):

    def __init__(self, l_operands, factor=1, power=1, derivative=0):
        super().__init__(factor, power, derivative)
        self.l_operands = l_operands
        self.collapse()
    # Need to implement sum and mult equivalences
    # without assuming lists are ordered.


class SumExpression(OpExpression):

    def differentiate(self):
        return SumExpression(
            map(lambda expr: expr.differentiate(), self.l_operands))

    def collapse(self):
        l_new_operands = [self.l_operands[0]]
        for i_old_operand in range(1, len(self.l_operands)):
            added = False
            old_operand = self.l_operands[i_old_operand]
            for new_operand in l_new_operands:
                if new_operand.is_add_equiv(old_operand):
                    added = True
                    new_operand.factor += old_operand.factor
                    break
            if not added:
                l_new_operands += [old_operand]


class ProductExpression(OpExpression):

    def differentiate(self):
        return SumExpression(map(self._differentiate_i, range(
            len(self.l_operands))))  # Might not like to be curried

    def _differentiate_i(self, i):
        l_new_operands = self.l_operands
        l_new_operands[i] = l_new_operands[i].differentiate()
        return ProductExpression(l_new_operands)

    def collapse(self):
        l_new_operands = [self.l_operands[0]]
        for i_old_operand in range(1, len(self.l_operands)):
            added = False
            old_operand = self.l_operands[i_old_operand]
            for new_operand in l_new_operands:
                if new_operand.is_mult_equiv(old_operand):
                    added = True
                    new_operand.power += old_operand.power
                    new_operand.factor *= old_operand.factor
                    break
            if not added:
                l_new_operands += [old_operand]


class Function(Expression):

    def __init__(self, name, factor=1, power=1, derivative=0):
        self.name = name
        super().__init__(factor, power, derivative)
        # if self. # Need to deal with power = 0

    def is_mult_equiv(self, other):
        return all([self.name == other.name,
                    self.derivative == other.derivative])

    def is_add_equiv(self, other):
        return all([self.name == other.name,
                    self.derivative == other.derivative,
                    self.power == other.power])

    def differentiate(self):
        if power > 1:
            return ProductExpression(
                [Function(self.name, 1, self.power - 1, self.derivative),
                 Function(self.name, 1, 1, self.derivative + 1)],
                factor=self.factor * self.power)
        else:
            return Function(
                self.name,
                factor=self.factor,
                power=self.power,
                derivative=self.derivative+1)


class Constant(Expression):

    def __init__(self, value):
        self.value = value
        super().__init__()

    def differentiate(self):
        return Constant(0)

    def __mul__(self, other):
        return self.value * other

    def __rmul__(self, other):
        return other * self.value

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

# class Variable(Expression):
#   def __init__(self, name, substitution=None):
#       if (name in d_objects):
#           raise ValueError("An object named '{}' already exists".format(name))
#       self.name = name
#       self.substitution = substitution

#       d_objects[name] = self

#       if self.substitution:
#           self.differentiate = substitution.differentiate
#       else:
#           self.differentiate = lambda (): Constant(1)

#!/usr/bin/env python3

# An implementation of symbols for the simplest equation method

# Assuming one function, one variable

# I originally wanted to avoid relying on canonical forms, since I'll inevitably
# screw up the canonization, but that really does seem like the best way to go
# at this point.

from abc import ABC, abstractmethod

d_objects = {}


class Expression(ABC):

    def __init__(self, base, factor=1, power=1, derivative=0):
        self.base = base
        self.factor = factor
        self.power = power
        self.derivative = derivative

    @abstractmethod
    def canonize(self):
        pass

    def differentiate(self):
        # This method will likely be subsumed in the coming op'ization
        if self.power > 1:
            power_decrement = self.copy()
            power_decrement.power -= 1
            base_derivative = self.copy()
            base
            base_derivative.derivative += 1
            return OpExpression(
                MultOp,
                [Function(self.name, 1, self.power - 1, self.derivative),
                 Function(self.name, 1, 1, self.derivative + 1)],
                factor=self.factor * self.power)
        else:
            return Function(
                self.name,
                factor=self.factor,
                power=self.power,
                derivative=self.derivative+1)


class OpExpression(Expression):

    def __init__(self, op, l_operands, factor=1, power=1, derivative=0):
        super().__init__(factor, power, derivative)
        self.op = op
        self.l_operands = l_operands
        self.collapse()

    def collapse(self):
        """
            Use the op to combine terms that can be combined.

            Initializes the new list of operands to have the first "old"
            operand, then iterates through the "old operands," which is to
            say the current list of operands. For each old operand, attempt
            to combine with any existing "new" operands. When you find a valid
            combination, stop, and replace the combinable "new" operand with
            the new combination. If no such combinations are possible, then
            add the "old" operand to the new list.
        """
        # This should be refactored, so that Op has most of this machinery
        l_new_opds = [self.l_operands[0]]  # opd is operand
        for old_opd in self.l_operands[1:]:
            combined_opd = None
            i_combined = None
            for i_new_opd, new_opd in enumerate(l_new_opds):
                combined_opd = self.op.combine(old_opd, new_opd)
                if combined_opd:
                    i_combined = i_new_opd
                    break
            if combined_opd:
                l_new_opds[i_combined] = combined_opd
            else:
                l_new_opds += [old_opd]


class Op(ABC):
    """
        Never instantiated.
        All static methods. Parallel problems? Not sure.
    """
    @abstractmethod
    def string():
        pass

    @abstractmethod
    def apply(*l_operands):
        pass

    @abstractmethod
    def derivative(*l_operands):
        pass


class SumOp(Op):

    @staticmethod
    def string():
        return '+'

    @staticmethod
    def apply(*l_operands):
        assert len(l_operands) == 2  # shouldn't be assert
        opd1, opd2 = l_operands
        if opd1.base == opd2.base and opd1.power == opd2.power and opd1.derivative == opd2.derivative:
            new_opd = opd1.copy()
            new_opd.factor += opd2.factor
            return new_opd
        else:
            return None

    @staticmethod
    def derivative(*l_operands):
        return OpExpression(SumOp,
                            map(lambda x: x.derivative(), l_operands))


class MultOp(Op):

    @staticmethod
    def string():
        return ''

    @staticmethod
    def apply(*l_operands):
        assert len(l_operands) == 2  # still shouldn't be assert
        opd1, opd2 = l_operands
        if opd1.base == opd2.base and opd1.derivative == opd2.derivative:
            new_opd = opd1.copy()
            new_opd.factor *= opd2.factor
            new_opd.power += opd2.power
            return new_opd
        else:
            return None

    @staticmethod
    def derivative(*l_operands):
        l_new_opds = [[opd.copy() for opd in l_operands] for x in l_operands]
        l_prod_exprs = []
        for dx in range(len(l_operands)):
            l_new_opds[dx][dx] = l_new_opds[dx][dx].derivative()
            l_prod_exprs += [OpExpression(MultOp, l_new_opds[dx])]
        return OpExpression(SumOp, l_prod_exprs)


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

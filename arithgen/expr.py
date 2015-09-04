"""Define expression types."""

from abc import ABCMeta, abstractmethod
from fractions import Fraction


class Expression(metaclass=ABCMeta):
    """Base class for expressions."""

    # Order of operation for binary operators, should be None for
    # anything else.
    level = None

    def __init__(self, *, name=None):
        self.name = name

    def __str__(self):
        return format(self, '')

    def __format__(self, fmt):
        if self.name is not None:
            return self.name
        if not fmt:
            return self.to_string()
        if fmt == 'rpn':
            return self.to_reverse_polish()
        raise ValueError('Unrecognized format string {!r}'.format(fmt))

    @abstractmethod
    def to_string(self):
        """Return infix notation of the expression."""

    @abstractmethod
    def to_reverse_polish(self):
        """Return reverse polish notation of the expression."""

    @abstractmethod
    def evaluate(self):
        """Return evaluated result of the expression."""


class Integer(Expression):
    """An integer."""

    def __init__(self, num, *, name=None):
        super().__init__(name=name)
        self._num = num

    def to_string(self):
        return str(self._num)

    def to_reverse_polish(self):
        return str(self._num)

    def evaluate(self):
        return Fraction(self._num)


class BinaryExpression(Expression):
    """A binary expression."""

    # Subtraction and division
    is_negative = False

    def __init__(self, oper, left, right, *, name=None):
        super().__init__(name=name)
        self._oper = oper
        self._left = left
        self._right = right

    def to_string(self):
        left_part = str(self._left)
        if (self._left.level is not None and
                self._left.level < self.level):
            left_part = '(' + left_part + ')'
        right_part = str(self._right)
        if (self._right.level is not None and
                (self._right.level < self.level or
                 self._right.level == self.level and
                 self.is_negative)):
            right_part = '(' + right_part + ')'
        return left_part + ' ' + str(self._oper) + ' ' + right_part

    def to_reverse_polish(self):
        return '{left:rpn} {right:rpn} {oper}'.format(
            oper=self._oper,
            left=self._left,
            right=self._right,
        )

    @abstractmethod
    def evaluate(self):
        """Return evaluated binary expression."""


class Addition(BinaryExpression):
    """a + b expressions."""

    level = 1

    def __init__(self, left, right, *, name=None):
        super().__init__('+', left, right, name=name)

    def evaluate(self):
        return self._left.evaluate() + self._right.evaluate()


class Subtraction(BinaryExpression):
    """a - b expressions."""

    level = 1
    is_negative = True

    def __init__(self, left, right, *, name=None):
        super().__init__('-', left, right, name=name)

    def evaluate(self):
        return self._left.evaluate() - self._right.evaluate()


class Multiplication(BinaryExpression):
    """a * b expressions."""

    level = 2

    def __init__(self, left, right, *, name=None):
        super().__init__('*', left, right, name=name)

    def evaluate(self):
        return self._left.evaluate() * self._right.evaluate()


class Division(BinaryExpression):
    """a / b expressions."""

    level = 2
    is_negative = True

    def __init__(self, left, right, *, name=None):
        super().__init__('/', left, right, name=name)

    def evaluate(self):
        return self._left.evaluate() / self._right.evaluate()

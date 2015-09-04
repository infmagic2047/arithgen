"""Core of arithgen."""

import math
import random
from fractions import Fraction

from arithgen import ntheory
from arithgen.expr import (
    Integer,
    Addition,
    Subtraction,
    Multiplication,
    Division,
)


def weighted_choice(choices):
    """Return a weighted random element from a non-empty sequence.

    choices is a sequence of two-element sequences. The first element of
    each sequence is the element and the second one is the weight.
    """
    total = sum(weight for element, weight in choices)
    r = random.uniform(0, total)
    upto = 0
    for element, weight in choices:
        upto += weight
        if upto >= r:
            return element
    assert False, 'Should never get here'


class NumPrimeGenerator:
    """Generate numbers with only a given set of prime factors."""

    def __init__(self, primes):
        self._primes = frozenset(primes)

    def is_valid(self, x, maxval=None):
        """Check whether x has only the given set of prime factors."""
        if x <= 0 or (maxval is not None and x > maxval):
            return False
        t = x
        for i in self._primes:
            while t % i == 0:
                t /= i
        return t == 1

    def gen_number(self, maxval):
        """Generate a number."""
        return self.gen_pairwise_coprime_numbers((maxval,))[0]

    def gen_coprime_numbers(self, maxval1, maxval2):
        """Generate two coprime numbers."""
        return self.gen_pairwise_coprime_numbers((maxval1, maxval2))

    def gen_pairwise_coprime_numbers(self, maxvals):
        """Generate a list of pairwise coprime numbers."""
        pr_choices = set(self._primes)
        pr_used = {pr: None for pr in self._primes}
        vals = [1] * len(maxvals)
        while pr_choices:
            now = weighted_choice([(pr, math.log(pr) / pr)
                                   for pr in pr_choices])
            if pr_used[now] is None:
                pos_choices = [x for x in range(len(maxvals))
                               if vals[x] * now <= maxvals[x]]
                if not pos_choices:
                    # The current prime will be removed anyway, give it
                    # an arbitrary index
                    pos_choices = [0]
                pr_used[now] = random.choice(pos_choices)
            x = pr_used[now]
            if vals[x] * now > maxvals[x]:
                pr_choices.remove(now)
            else:
                vals[x] *= now
        return vals

    def gen_numbers_with_sum(self, maxval, result, trials=100):
        """Generate a, b with a + b = result.

        Return None if generation failed.
        """
        for _ in range(trials):
            x = self.gen_number(min(maxval, result))
            if self.is_valid(result - x, maxval):
                if random.random() < 0.5:
                    return x, result - x
                else:
                    return result - x, x
        return None

    def gen_numbers_with_difference(self, maxval, result, trials=100):
        """Generate a, b with a - b = result.

        Return None if generation failed.
        """
        for _ in range(trials):
            x = self.gen_number(maxval)
            if self.is_valid(x - result, maxval):
                return x, x - result
            if self.is_valid(x + result, maxval):
                return x + result, x
        return None


class ExprGenerator:
    def __init__(self, difficulty):
        self._difficulty = difficulty
        self._maxval = 10 * 2 ** difficulty
        self._numgen = None

    def _gen_primes(self):
        primecnt = 2 + int(1.5 * self._difficulty)
        prime_ind = [1] + random.sample(range(2, int(1.5 * primecnt)),
                                        primecnt - 1)
        primes = [ntheory.prime(i) for i in prime_ind]
        self._numgen = NumPrimeGenerator(primes)

    def _ending_prob(self, depth):
        # Probability table:
        # difficulty\depth  0       1       2       3       4
        # 1                 0       0.5     0.9     0.9     0.9
        # 2                 0       0.2     0.9     0.9     0.9
        # 3                 0       0       0.8     0.9     0.9
        # 4                 0       0       0.5     0.9     0.9
        # 5                 0       0       0.2     0.9     0.9
        min_depth = self._difficulty // 3 + 1
        if depth < min_depth:
            return 0
        if depth == min_depth:
            return [0.8, 0.5, 0.2][self._difficulty % 3]
        return 0.9

    def _gen_division_operand(self, result):
        left = result.numerator
        right = result.denominator
        numerator, denominator = self._numgen.gen_coprime_numbers(
            self._maxval // max(left, right), self._maxval)
        mult_frac = Fraction(numerator, denominator)
        left *= mult_frac
        right *= mult_frac
        return left, right

    @property
    def op_gen_methods(self):
        return [
            self.gen_addition_with_result,
            self.gen_subtraction_with_result,
            self.gen_multiplication_with_result,
            self.gen_division_with_result,
        ]

    def gen_fraction(self):
        """Generate a random fraction."""
        numerator, denominator = self._numgen.gen_coprime_numbers(
            self._maxval, self._maxval)
        return Fraction(numerator, denominator)

    def gen_addition_with_result(self, result, depth=0):
        """Generate a, b with a + b = result.

        Return None if generation failed.
        """
        pair = self._numgen.gen_numbers_with_sum(
            self._maxval, result.numerator)
        if not pair:
            return None
        left = Fraction(pair[0], result.denominator)
        right = Fraction(pair[1], result.denominator)
        return Addition(
            self.gen_expr_with_result(left, depth + 1, [1, 1, 2, 2]),
            self.gen_expr_with_result(right, depth + 1, [1, 1, 2, 2]),
        )

    def gen_subtraction_with_result(self, result, depth=0):
        """Generate a, b with a - b = result.

        Return None if generation failed.
        """
        pair = self._numgen.gen_numbers_with_difference(
            self._maxval, result.numerator)
        if not pair:
            return None
        left = Fraction(pair[0], result.denominator)
        right = Fraction(pair[1], result.denominator)
        return Subtraction(
            self.gen_expr_with_result(left, depth + 1, [1, 1, 2, 2]),
            self.gen_expr_with_result(right, depth + 1, [1, 1, 2, 2]),
        )

    def gen_multiplication_with_result(self, result, depth=0):
        """Generate a, b with a * b = result."""
        left, right = self._gen_division_operand(result)
        right = 1 / right
        return Multiplication(
            self.gen_expr_with_result(left, depth + 1, [2, 2, 1, 1]),
            self.gen_expr_with_result(right, depth + 1, [2, 2, 1, 1]),
        )

    def gen_division_with_result(self, result, depth=0):
        """Generate a, b with a / b = result."""
        left, right = self._gen_division_operand(result)
        return Division(
            self.gen_expr_with_result(left, depth + 1, [2, 2, 1, 1]),
            self.gen_expr_with_result(right, depth + 1, [2, 2, 1, 1]),
        )

    def gen_expr_with_result(self, result, depth=0, op_weight=None):
        """Generate a random expression with given result."""
        if op_weight is None:
            op_weight = [1, 1, 1, 1]
        if random.random() < self._ending_prob(depth):
            if result.denominator == 1:
                return Integer(result.numerator)
            return Division(
                Integer(result.numerator),
                Integer(result.denominator),
            )
        ans = None
        while ans is None:
            meth = weighted_choice(list(zip(self.op_gen_methods,
                                            op_weight)))
            ans = meth(result, depth)
        return ans

    def gen_expr(self):
        """Generate a random expression and the result."""
        self._gen_primes()
        result = self.gen_fraction()
        return self.gen_expr_with_result(result), result


def generate(*, difficulty):
    """Generate a arithmetic expression."""
    gen = ExprGenerator(difficulty)
    return gen.gen_expr()

import unittest

from fractions import Fraction

from arithgen.expr import (
    Integer,
    Addition,
    Subtraction,
    Multiplication,
    Division,
)


class TestExprEvaluation(unittest.TestCase):
    def test_integer(self):
        expr = Integer(9)
        self.assertEqual(expr.evaluate(), 9)

    def test_addition(self):
        expr = Addition(Integer(5), Integer(6))
        self.assertEqual(expr.evaluate(), 11)

    def test_subtraction(self):
        expr = Subtraction(Integer(4), Integer(7))
        self.assertEqual(expr.evaluate(), -3)

    def test_multiplication(self):
        expr = Multiplication(Integer(3), Integer(8))
        self.assertEqual(expr.evaluate(), 24)

    def test_division(self):
        expr = Division(Integer(8), Integer(6))
        self.assertEqual(expr.evaluate(), Fraction(4, 3))

    def test_compound(self):
        expr = Division(
            Addition(
                Integer(4),
                Division(Integer(2), Integer(5)),
            ),
            Multiplication(
                Subtraction(
                    Multiplication(Integer(2), Integer(4)),
                    Division(Integer(6), Integer(5)),
                ),
                Addition(
                    Division(Integer(3), Integer(2)),
                    Division(Integer(4), Integer(3)),
                ),
            ),
        )
        self.assertEqual(expr.evaluate(), Fraction(66, 289))


class TestExprConvertToString(unittest.TestCase):
    def test_infix(self):
        expr = Addition(
            Subtraction(
                Division(
                    Multiplication(
                        Integer(3),
                        Integer(4),
                    ),
                    Multiplication(
                        Integer(2),
                        Integer(6),
                    ),
                ),
                Division(
                    Integer(3),
                    Addition(
                        Integer(5),
                        Integer(6),
                    ),
                ),
            ),
            Multiplication(
                Subtraction(
                    Addition(
                        Integer(4),
                        Integer(2),
                    ),
                    Subtraction(
                        Integer(2),
                        Integer(1),
                    ),
                ),
                Integer(6),
            ),
        )
        self.assertEqual(expr.to_string(),
                         '3 * 4 / (2 * 6) - 3 / (5 + 6) + '
                         '(4 + 2 - (2 - 1)) * 6')

    def test_reverse_polish(self):
        expr = Addition(
            Subtraction(
                Division(
                    Multiplication(
                        Integer(3),
                        Integer(4),
                    ),
                    Multiplication(
                        Integer(2),
                        Integer(6),
                    ),
                ),
                Division(
                    Integer(3),
                    Addition(
                        Integer(5),
                        Integer(6),
                    ),
                ),
            ),
            Multiplication(
                Subtraction(
                    Addition(
                        Integer(4),
                        Integer(2),
                    ),
                    Subtraction(
                        Integer(2),
                        Integer(1),
                    ),
                ),
                Integer(6),
            ),
        )
        self.assertEqual(expr.to_reverse_polish(),
                         '3 4 * 2 6 * / 3 5 6 + / - '
                         '4 2 + 2 1 - - 6 * +')


if __name__ == '__main__':
    unittest.main()

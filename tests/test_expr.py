from fractions import Fraction

from arithgen import expr


def test_integer():
    e = expr.Integer(9)
    assert e.evaluate() == 9


def test_addition():
    e = expr.Addition(expr.Integer(5), expr.Integer(6))
    assert e.evaluate() == 11


def test_subtraction():
    e = expr.Subtraction(expr.Integer(4), expr.Integer(7))
    assert e.evaluate() == -3


def test_multiplication():
    e = expr.Multiplication(expr.Integer(3), expr.Integer(8))
    assert e.evaluate() == 24


def test_division():
    e = expr.Division(expr.Integer(8), expr.Integer(6))
    assert e.evaluate() == Fraction(4, 3)


def test_compound():
    e = expr.Division(
        expr.Addition(
            expr.Integer(4),
            expr.Division(expr.Integer(2), expr.Integer(5)),
        ),
        expr.Multiplication(
            expr.Subtraction(
                expr.Multiplication(expr.Integer(2), expr.Integer(4)),
                expr.Division(expr.Integer(6), expr.Integer(5)),
            ),
            expr.Addition(
                expr.Division(expr.Integer(3), expr.Integer(2)),
                expr.Division(expr.Integer(4), expr.Integer(3)),
            ),
        ),
    )
    assert e.evaluate() == Fraction(66, 289)


def test_string_infix():
    e = expr.Addition(
        expr.Subtraction(
            expr.Division(
                expr.Multiplication(expr.Integer(3), expr.Integer(4)),
                expr.Multiplication(expr.Integer(2), expr.Integer(6)),
            ),
            expr.Division(
                expr.Integer(3),
                expr.Addition(expr.Integer(5), expr.Integer(6)),
            ),
        ),
        expr.Multiplication(
            expr.Subtraction(
                expr.Addition(expr.Integer(4), expr.Integer(2)),
                expr.Subtraction(expr.Integer(2), expr.Integer(1)),
            ),
            expr.Integer(6),
        ),
    )
    assert (e.to_string() ==
            '3 * 4 / (2 * 6) - 3 / (5 + 6) + (4 + 2 - (2 - 1)) * 6')


def test_string_reverse_polish():
    e = expr.Addition(
        expr.Subtraction(
            expr.Division(
                expr.Multiplication(expr.Integer(3), expr.Integer(4)),
                expr.Multiplication(expr.Integer(2), expr.Integer(6)),
            ),
            expr.Division(
                expr.Integer(3),
                expr.Addition(expr.Integer(5), expr.Integer(6)),
            ),
        ),
        expr.Multiplication(
            expr.Subtraction(
                expr.Addition(expr.Integer(4), expr.Integer(2)),
                expr.Subtraction(expr.Integer(2), expr.Integer(1)),
            ),
            expr.Integer(6),
        ),
    )
    assert (e.to_reverse_polish() ==
            '3 4 * 2 6 * / 3 5 6 + / - 4 2 + 2 1 - - 6 * +')

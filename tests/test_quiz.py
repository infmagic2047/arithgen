from fractions import Fraction

import pytest

from arithgen import quiz


def test_parse_fraction_strict():
    assert quiz.parse_fraction_strict('0') == 0
    assert quiz.parse_fraction_strict('12') == 12
    assert quiz.parse_fraction_strict('2/13') == Fraction(2, 13)
    with pytest.raises(ValueError):
        quiz.parse_fraction_strict('-1')
    with pytest.raises(ValueError):
        quiz.parse_fraction_strict('0123')
    with pytest.raises(ValueError):
        quiz.parse_fraction_strict('0x123')
    with pytest.raises(ValueError):
        quiz.parse_fraction_strict('0001')
    with pytest.raises(ValueError):
        quiz.parse_fraction_strict('-1/123')
    with pytest.raises(ValueError):
        quiz.parse_fraction_strict('0/123')
    with pytest.raises(ValueError):
        quiz.parse_fraction_strict('4/6')
    with pytest.raises(ValueError):
        quiz.parse_fraction_strict('5/1')
    with pytest.raises(ValueError):
        quiz.parse_fraction_strict('1/0')

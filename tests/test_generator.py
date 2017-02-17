import itertools
import math
import random

import pytest

from arithgen import generator


def test_is_valid():
    gen = generator.NumPrimeGenerator([2, 5, 7, 13])
    assert gen.is_valid(1)
    assert gen.is_valid(7)
    assert gen.is_valid(52)
    assert gen.is_valid(384475)
    assert not gen.is_valid(-1)
    assert not gen.is_valid(0)
    assert not gen.is_valid(30)
    assert not gen.is_valid(176)
    assert gen.is_valid(70, 100)
    assert not gen.is_valid(70, 50)


@pytest.mark.parametrize('maxvals, count', [
    ((1000,), 100),
    ((100, 1000), 100),
    ((400, 200, 300, 100), 100),
])
def test_gen_pairwise_coprime_numbers(maxvals, count):
    random.seed(12345)
    gen = generator.NumPrimeGenerator([2, 3, 7, 13, 17, 29])
    for _ in range(count):
        vals = gen.gen_pairwise_coprime_numbers(maxvals)
        assert len(vals) == len(maxvals)
        for val, maxval in zip(vals, maxvals):
            assert gen.is_valid(val, maxval)
        for x, y in itertools.combinations(vals, 2):
            assert math.gcd(x, y) == 1


def test_gen_numbers_with_sum():
    random.seed(23456)
    gen = generator.NumPrimeGenerator([2, 7, 13, 29])
    maxval = 1000
    success_count = 0
    for i in range(1000, 1500):
        pair = gen.gen_numbers_with_sum(maxval, i, 10)
        if pair is not None:
            assert len(pair) == 2
            assert gen.is_valid(pair[0], maxval)
            assert gen.is_valid(pair[1], maxval)
            assert pair[0] + pair[1] == i
            success_count += 1
    # At least some reasonable number of success
    assert success_count >= 50


def test_gen_numbers_with_difference():
    random.seed(23456)
    gen = generator.NumPrimeGenerator([2, 7, 13, 29])
    maxval = 2000
    success_count = 0
    for i in range(1000, 1500):
        pair = gen.gen_numbers_with_difference(maxval, i, 10)
        if pair is not None:
            assert len(pair) == 2
            assert gen.is_valid(pair[0], maxval)
            assert gen.is_valid(pair[1], maxval)
            assert pair[0] - pair[1] == i
            success_count += 1
    # At least some reasonable number of success
    assert success_count >= 50


@pytest.mark.parametrize('difficulty, count', [
    (1, 200),
    (2, 80),
    (3, 30),
    (5, 15),
    (10, 3),
])
def test_gen_expr(difficulty, count):
    random.seed(34567)
    gen = generator.ExprGenerator(difficulty)
    for _ in range(count):
        e, result = gen.gen_expr()
        assert e.evaluate() == result

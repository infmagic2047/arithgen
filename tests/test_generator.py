import unittest

import random
from fractions import gcd
from itertools import combinations

from arithgen.generator import NumPrimeGenerator, ExprGenerator


class TestNumPrimeGenerator(unittest.TestCase):
    def test_is_valid(self):
        gen = NumPrimeGenerator([2, 5, 7, 13])
        self.assertTrue(gen.is_valid(1))
        self.assertTrue(gen.is_valid(7))
        self.assertTrue(gen.is_valid(52))
        self.assertTrue(gen.is_valid(384475))
        self.assertFalse(gen.is_valid(-1))
        self.assertFalse(gen.is_valid(-0))
        self.assertFalse(gen.is_valid(30))
        self.assertFalse(gen.is_valid(176))
        self.assertTrue(gen.is_valid(70, 100))
        self.assertFalse(gen.is_valid(70, 50))

    def test_gen_pairwise_coprime_numbers(self):
        gen = NumPrimeGenerator([2, 3, 7, 13, 17, 29])
        random.seed(12345)
        test_cases = [
            ((100,), 1000),
            ((500,), 300),
            ((1000,), 100),
            ((200, 200), 500),
            ((100, 1000), 500),
            ((100, 500, 300), 300),
            ((400, 200, 300, 100), 100),
        ]
        for maxvals, test_count in test_cases:
            for i in range(test_count):
                with self.subTest(maxvals=maxvals, i=i):
                    vals = gen.gen_pairwise_coprime_numbers(maxvals)
                    self.assertEqual(len(vals), len(maxvals))
                    for val, maxval in zip(vals, maxvals):
                        self.assertTrue(gen.is_valid(val, maxval))
                    for pair in combinations(vals, 2):
                        self.assertEqual(gcd(pair[0], pair[1]), 1)

    def test_gen_numbers_with_sum(self):
        gen = NumPrimeGenerator([2, 7, 13, 29])
        random.seed(23456)
        maxval = 1000
        success_count = 0
        for i in range(1000, 1500):
            with self.subTest(i=i):
                pair = gen.gen_numbers_with_sum(maxval, i, 10)
                if pair is not None:
                    self.assertEqual(len(pair), 2)
                    success_count += 1
                    self.assertTrue(gen.is_valid(pair[0], maxval))
                    self.assertTrue(gen.is_valid(pair[1], maxval))
                    self.assertEqual(pair[0] + pair[1], i)
        # At least some reasonable number of success
        self.assertGreaterEqual(success_count, 50)

    def test_gen_numbers_with_difference(self):
        gen = NumPrimeGenerator([2, 7, 13, 29])
        random.seed(23456)
        maxval = 2000
        success_count = 0
        for i in range(1000, 1500):
            with self.subTest(i=i):
                pair = gen.gen_numbers_with_difference(maxval, i, 10)
                if pair is not None:
                    self.assertEqual(len(pair), 2)
                    success_count += 1
                    self.assertTrue(gen.is_valid(pair[0], maxval))
                    self.assertTrue(gen.is_valid(pair[1], maxval))
                    self.assertEqual(pair[0] - pair[1], i)
        # At least some reasonable number of success
        self.assertGreaterEqual(success_count, 50)


class TestExprGenerator(unittest.TestCase):
    def test_gen_expr(self):
        random.seed(34567)
        test_cases = [
            (1, 200),
            (2, 80),
            (3, 30),
            (5, 15),
            (10, 3),
        ]
        for difficulty, test_count in test_cases:
            gen = ExprGenerator(difficulty)
            for i in range(test_count):
                with self.subTest(difficulty=difficulty, i=i):
                    expr, result = gen.gen_expr()
                    self.assertEqual(expr.evaluate(), result)


if __name__ == '__main__':
    unittest.main()

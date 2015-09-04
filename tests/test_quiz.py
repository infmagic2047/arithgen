import unittest

from fractions import Fraction

from arithgen.quiz import parse_args, parse_fraction_strict


class TestArgParser(unittest.TestCase):
    def test_parsing(self):
        args = parse_args(['-d11', '--strict'])
        self.assertEqual(args.difficulty, 11)
        self.assertEqual(args.strict, True)


class TestParseFractionStrict(unittest.TestCase):
    def test_parsing(self):
        self.assertEqual(parse_fraction_strict('0'), Fraction(0))
        self.assertEqual(parse_fraction_strict('12'), Fraction(12))
        self.assertEqual(parse_fraction_strict('2/13'), Fraction(2, 13))
        self.assertRaises(ValueError, parse_fraction_strict, '-1')
        self.assertRaises(ValueError, parse_fraction_strict, '0123')
        self.assertRaises(ValueError, parse_fraction_strict, '0x123')
        self.assertRaises(ValueError, parse_fraction_strict, '0001')
        self.assertRaises(ValueError, parse_fraction_strict, '-1/123')
        self.assertRaises(ValueError, parse_fraction_strict, '0/123')
        self.assertRaises(ValueError, parse_fraction_strict, '4/6')
        self.assertRaises(ValueError, parse_fraction_strict, '5/1')
        self.assertRaises(ValueError, parse_fraction_strict, '1/0')


if __name__ == '__main__':
    unittest.main()

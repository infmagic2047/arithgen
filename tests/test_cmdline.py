import unittest

from arithgen.cmdline import parse_args


class TestArgParser(unittest.TestCase):
    def test_parsing(self):
        args = parse_args(['-n7', '-d11'])
        self.assertEqual(args.count, 7)
        self.assertEqual(args.difficulty, 11)


if __name__ == '__main__':
    unittest.main()

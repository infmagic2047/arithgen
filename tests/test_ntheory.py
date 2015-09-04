import unittest

from arithgen.ntheory import isprime, nextprime, prevprime, prime


class TestPrimes(unittest.TestCase):
    def test_isprime(self):
        self.assertEqual(isprime(-5), False)
        self.assertEqual(isprime(0), False)
        self.assertEqual(isprime(1), False)
        self.assertEqual(isprime(2), True)
        self.assertEqual(isprime(3), True)
        self.assertEqual(isprime(67), True)
        self.assertEqual(isprime(191), True)
        self.assertEqual(isprime(561), False)

    def test_nextprime(self):
        self.assertEqual(nextprime(10), 11)
        self.assertEqual(nextprime(123), 127)
        self.assertEqual(nextprime(89), 97)
        self.assertEqual(nextprime(1), 2)
        self.assertEqual(nextprime(50, 4), 67)
        self.assertEqual(nextprime(41, 2), 47)

    def test_prevprime(self):
        self.assertEqual(prevprime(15), 13)
        self.assertEqual(prevprime(83), 79)
        self.assertEqual(prevprime(3), 2)
        self.assertRaises(ValueError, prevprime, 2)
        self.assertRaises(ValueError, prevprime, 0)

    def test_prime(self):
        self.assertEqual(prime(1), 2)
        self.assertEqual(prime(27), 103)
        self.assertRaises(ValueError, prime, 0)
        self.assertRaises(ValueError, prime, -1)


if __name__ == '__main__':
    unittest.main()

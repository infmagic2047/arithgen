"""Number theory functions.

The implementations here use naive algorithms, so they should not be
called with large data.
"""

import math


def isprime(n):
    """Test whether n is a prime or not."""
    if n == 2:
        return True
    if n < 2 or n % 2 == 0:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))


def nextprime(n, ith=1):
    """Return the ith prime greater than n."""
    if ith > 1:
        pr = n
        for _ in range(ith):
            pr = nextprime(pr)
        return pr
    pr = n + 1
    while not isprime(pr):
        pr += 1
    return pr


def prevprime(n):
    """Return largest prime smaller than n."""
    if n < 3:
        raise ValueError('No primes smaller than {!r}'.format(n))
    pr = n - 1
    while not isprime(pr):
        pr -= 1
    return pr


def prime(nth):
    """Return the nth prime."""
    if nth < 1:
        raise ValueError('nth must be a positive integer')
    return nextprime(1, nth)

import pytest

from arithgen import ntheory


def test_isprime():
    assert not ntheory.isprime(-5)
    assert not ntheory.isprime(0)
    assert not ntheory.isprime(1)
    assert ntheory.isprime(2)
    assert ntheory.isprime(3)
    assert ntheory.isprime(67)
    assert ntheory.isprime(191)
    assert not ntheory.isprime(561)


def test_nextprime():
    assert ntheory.nextprime(10) == 11
    assert ntheory.nextprime(123) == 127
    assert ntheory.nextprime(89) == 97
    assert ntheory.nextprime(1) == 2
    assert ntheory.nextprime(50, 4) == 67
    assert ntheory.nextprime(41, 2) == 47


def test_prevprime():
    assert ntheory.prevprime(15) == 13
    assert ntheory.prevprime(83) == 79
    assert ntheory.prevprime(3) == 2
    with pytest.raises(ValueError):
        ntheory.prevprime(2)
    with pytest.raises(ValueError):
        ntheory.prevprime(0)


def test_prime():
    assert ntheory.prime(1) == 2
    assert ntheory.prime(27) == 103
    with pytest.raises(ValueError):
        ntheory.prime(0)
    with pytest.raises(ValueError):
        ntheory.prime(-1)

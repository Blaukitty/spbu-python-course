import pytest
from project.curring import curry_explicit, uncurry_explicit


@pytest.fixture
def summa():
    def suma(a, b):
        return a + b
    return suma

def test_basic(summa):
    curr = curry_explicit(summa, 2)
    result = curr(1)(2)
    assert result == 3

def test_zero_arity():
    def zero_ar():
        return 0
    curr = curry_explicit(zero_ar, 0)
    result = curr()
    assert result == 0

def test_one_arity():
    def one_ar(x):
        return x
    curr = curry_explicit(one_ar, 1)
    result = curr(1)
    assert result == 1

def test_print():
    curr = curry_explicit(print, 2)
    result = curr(1)(2)
    assert result is None


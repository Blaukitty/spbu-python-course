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


def test_zero():
    def zero_ar():
        return 0

    curr = curry_explicit(zero_ar, 0)
    result = curr()
    assert result == 0


def test_one():
    def one_ar(x):
        return x

    curr = curry_explicit(one_ar, 1)
    result = curr(1)
    assert result == 1
    

def test_curry_fixes_arity():
    """curry_explicit freezes arity for arbitrary-ary functions"""
    
    curried_print = curry_explicit(print, 2)
    result = curried_print("Hello")("World")
    assert result is None
    
    with pytest.raises(TypeError, match="'NoneType' object is not callable"):
        curried_print("Hello")("World")("Extra")
    
    with pytest.raises(ValueError, match="Function expects 2 arguments, but 3 were given"):
        curried_print("Hello", "World", "Extra")


def test_unpositiv(summa):
    with pytest.raises(ValueError):
        result = curry_explicit(summa, -2)


def test_mistake(summa):
    with pytest.raises(ValueError):
        result = curry_explicit(summa, 10)


def test_unpositiv_un(summa):
    with pytest.raises(ValueError):
        result = uncurry_explicit(summa, -2)


def test_mistake_un(summa):
    with pytest.raises(ValueError):
        result = uncurry_explicit(summa, 10)


def test_uncurry(summa):
    curr = curry_explicit(summa, 2)
    uncurr = uncurry_explicit(curr, 2)
    result = uncurr(1, 2)
    assert result == 3

@pytest.fixture
def three:
    def add_three(a, b, c):
        return a + b + c
    return add_three

def test_curry_no_multiple(three):
    """You cannot pass multiple arguments in a single call to a curried function"""    
    curried_add = curry_explicit(three, 3)
    
    with pytest.raises(ValueError, match="Function expects 1 arguments, but 2 were given"):
        curried_add(1, 2)(3)
    
    with pytest.raises(ValueError, match="Function expects 1 arguments, but 2 were given"):
        curried_add(1)(2, 3)
    
    with pytest.raises(ValueError, match="Function expects 1 arguments, but 3 were given"):
        curried_add(1, 2, 3)

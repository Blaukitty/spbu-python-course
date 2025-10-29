import pytest
from project.curring import curry_explicit, uncurry_explicit


@pytest.fixture
def summa():
    def suma(a, b):
        return a + b

    return suma


@pytest.fixture
def three():
    def add_three(a, b, c):
        return a + b + c

    return add_three


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


def test_curry_fixes_arity_for_max():
    """curry_explicit fixes arity for function max"""
    curried_max = curry_explicit(max, 2)

    result = curried_max(5)(10)
    assert result == 10

    with pytest.raises(TypeError, match="'int' object is not callable"):
        curried_max(5)(10)(15)

    with pytest.raises(ValueError, match="Function expects 2 arguments, but 3 were given"):
        curried_max(5, 10, 15)

    with pytest.raises(ValueError, match="Function expects 1 arguments, but 2 were given"):
        inter = curried_max(5)
        inter(10, 15)


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


def test_curry_no_multiple(three):
    """You cannot pass multiple arguments in a single call to a curried function"""
    curried_add = curry_explicit(three, 3)

    with pytest.raises(ValueError, match="Function expects 1 arguments, but 2 were given"):
        curried_add(1, 2)(3)

    with pytest.raises(ValueError, match="Function expects 1 arguments, but 2 were given"):
        curried_add(1)(2, 3)

    with pytest.raises(ValueError, match="Function expects 1 arguments, but 3 were given"):
        curried_add(1, 2, 3)

from polynomial import Polynomial
from math import isclose
from modular_ints import ModularInt
import pytest

def test_illegal_constructor():
    with pytest.raises(TypeError) as _:
        Polynomial((1,2,3))

def test_zero_equality():
    assert Polynomial([]) == Polynomial([])
    assert Polynomial([]) == Polynomial([0])
    assert Polynomial([]) == Polynomial([0, 0, 0])

def test_trivial_inequality():
    assert Polynomial([]) != Polynomial([1])

def test_complex_equality():
    assert Polynomial([1,"hello",3.0]) == Polynomial([1,"hello",3.0])

def test_zero_addition():
    p1 = Polynomial([]) + Polynomial([1,2,3])
    p2 = Polynomial([1,2,3])
    assert p1 == p2

def test_constant_addition_to_zero():
    p1 = Polynomial([])
    assert p1 + 5 == 5 + p1 == Polynomial([5])
    assert p1 + 0 == 0 + p1 == Polynomial([])

def test_constant_addition():
    p1 = Polynomial([2,5,3])
    assert p1 + 5 == 5 + p1 == Polynomial([7,5,3])
    assert p1 + 0 == 0 + p1 == p1

def test_integer_addition():
    p1 = Polynomial([2,5,3]) + Polynomial([4,-3])
    p2 = Polynomial([6,2,3])
    assert p1 == p2

def test_nonstandard_addition():
    p1 = Polynomial([[1,2], "hello ", {'a' : 'b'}]) + Polynomial([[3,4], "world"])
    p2 = Polynomial([[1,2,3,4], "hello world", {'a' : 'b'}])
    assert p1 == p2

def test_ring_addition_simple():
    x = ModularInt(2, 6)
    y = ModularInt(5, 6)
    p1 = Polynomial([x])
    p2 = Polynomial([y])
    assert p1 + p2 == Polynomial([1])
    assert p1 + p2 + p2 == Polynomial([])

def test_zero_multiplication():
    p1 = Polynomial([])
    p2 = Polynomial([1,2,3])
    assert p1 * p1 == p1
    assert p1 * p2 == p1
    assert p2 * p1 == p1

def test_scalar_multiplication():
    p1 = Polynomial([])
    p2 = Polynomial([1,2,3])
    p3 = Polynomial([5,10,15])
    c = 5
    assert p1 * c == p1 == c * p1
    assert c * p2 == p3 == p2 * c
    assert Polynomial(["ha", "bye"]) * 2 == Polynomial(["haha", "byebye"])

def test_multiplication():
    p1 = Polynomial([1,2])
    p2 = Polynomial([3,4,5])
    assert p1 * p2 == p2 * p1 == Polynomial([3,10,13,10])

def test_ring_multiplication_simple():
    x = ModularInt(2, 6)
    y = ModularInt(3, 6)
    p1 = Polynomial([x])
    p2 = Polynomial([y])
    assert p1 * p2 == Polynomial([])

def test_ring_multiplication_complex():
    x0 = ModularInt(0, 4)
    x1 = x0 + 1
    x2 = x1 + 1
    x3 = x2 + 1
    p1 = Polynomial([x3, x1, x0, x2])
    p2 = Polynomial([x2, x1, x2])
    assert p1 * p2 == Polynomial([2, 1, 3, 2, 2])

def test_zero_exponentiation():
    p1 = Polynomial([])
    assert p1 == p1 ** 1
    assert p1 == p1 ** 2
    assert p1 == p1 ** 1000000000

def test_exponentiation():
    p1 = Polynomial([1, 1])
    assert p1 ** 1 == p1
    assert p1 ** 2 == Polynomial([1, 2, 1])
    assert p1 ** 3 == Polynomial([1, 3, 3, 1])

def test_field_division():
    p1 = Polynomial([2,7,6])
    p2 = Polynomial([1,2])
    p3 = Polynomial([2,3])
    assert p1 // p2 == p3 
    assert p1 // p3 == p2

def test_illegal_ring_division():
    x0 = ModularInt(0, 4)
    x1 = x0 + 1
    x2 = x1 + 1
    x3 = x2 + 1
    p1 = Polynomial([x3, x1, x0, x2])
    p2 = Polynomial([x2, x1, x2])
    with pytest.raises(ValueError) as _:
        p1 // p2

def test_simple_legal_ring_division():
    x0 = ModularInt(0, 3)
    x1 = x0 + 1
    x2 = x1 + 1
    p1 = Polynomial([x0, x2])
    p2 = Polynomial([x1])
    assert p1 // p2 == Polynomial([0, 2])

def test_complex_legal_ring_division():
    x0 = ModularInt(0, 4)
    x1 = x0 + 1
    x2 = x1 + 1
    x3 = x2 + 1
    p1 = Polynomial([x3, x1, x0, x2])
    p2 = Polynomial([x2, x1, x1])
    assert p1 // p2 == Polynomial([2, 2])
    assert p1 % p2 == Polynomial([3, 3])
    assert p1 == p2 * Polynomial([2, 2]) + Polynomial([3, 3])

def test_immutability():
    p1 = Polynomial([1])
    p2 = p1
    p1 += Polynomial([2])
    assert p2 == Polynomial([1])

def test_evaluation_zero():
    p1 = Polynomial([])
    assert p1(5) == 0

def test_evaluation_zero_with_zeroelement():
    p1 = Polynomial([])
    assert p1(5, zero_element=[]) == []

def test_evaluation_nonzero_with_zeroelement():
    p1 = Polynomial([1,1,1])
    assert p1(5, zero_element=[]) == 31

def test_evaluation_on_integers():
    p1 = Polynomial([3,2,1])
    assert p1(0) == 3
    assert p1(1) == 6
    assert p1(-1) == 2

def test_evaluation_on_float():
    p1 = Polynomial([-2,0,1])
    assert isclose(p1(2**.5), 0, abs_tol=1e-09)
    assert isclose(p1(-(2**.5)), 0, abs_tol=1e-09)
    assert p1(0) == -2
    assert p1(1) == -1
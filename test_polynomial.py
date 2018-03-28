from polynomial import Polynomial

def test_zero_equality():
    assert Polynomial([]) == Polynomial([])

def test_trivial_inequality():
    assert Polynomial([]) != Polynomial([1])

def test_complex_equality():
    assert Polynomial([1,"hello",3.0]) == Polynomial([1,"hello",3.0])

def test_zero_addition():
    p1 = Polynomial([]) + Polynomial([1,2,3])
    p2 = Polynomial([1,2,3])
    assert p1 == p2

def test_integer_addition():
    p1 = Polynomial([2,5,3]) + Polynomial([4,-3])
    p2 = Polynomial([6,2,3])
    assert p1 == p2

def test_nonstandard_addition():
    p1 = Polynomial([[1,2], "hello ", {'a' : 'b'}]) + Polynomial([[3,4], "world"])
    p2 = Polynomial([[1,2,3,4], "hello world", {'a' : 'b'}])
    assert p1 == p2

def test_immutability():
    p1 = Polynomial([1])
    p2 = p1
    p1 += Polynomial([2])
    assert p2 == Polynomial([1])
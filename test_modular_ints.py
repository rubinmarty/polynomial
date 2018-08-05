from modular_ints import ModularInt
import pytest


def test_illegal_value_type():
    with pytest.raises(TypeError) as _:
        ModularInt(3.0, 2)


def test_illegal_modulus_type():
    with pytest.raises(TypeError) as _:
        ModularInt(3, 2.0)


def test_illegal_zero_modulus_value():
    with pytest.raises(ValueError) as _:
        ModularInt(3, 0)


def test_illegal_negative_modulus_value():
    with pytest.raises(ValueError) as _:
        ModularInt(3, -1)


def test_equality_identity():
    x = ModularInt(5, 3)
    y = ModularInt(5, 3)
    assert x == x
    assert x == y
    assert not x != x
    assert not x != y


def test_equality_different():
    x = ModularInt(5, 3)
    y = ModularInt(4, 3)
    assert x != y
    assert not x == y


def test_equality_when_values_differ():
    x = ModularInt(2, 3)
    y = ModularInt(-7, 3)
    z = 5
    assert x == y == z == x


def test_unequal_when_moduli_differ():
    x = ModularInt(2, 3)
    y = ModularInt(2, 4)
    assert x != y


def test_neg():
    assert ModularInt(2, 4) == -ModularInt(2, 4)
    assert ModularInt(2, 3) == -ModularInt(1, 3)
    assert ModularInt(0, 5) == -ModularInt(0, 5)


def test_cannot_add_different_moduli():
    with pytest.raises(ValueError) as _:
        ModularInt(2, 3) + ModularInt(2, 4)


def test_cannot_add_invalid_type():
    with pytest.raises(TypeError) as _:
        ModularInt(2, 3) + 2.0


def test_valid_addition():
    assert ModularInt(2, 3) + ModularInt(1, 3) == ModularInt(0, 3)
    assert ModularInt(4, 7) + 5 == ModularInt(2, 7)
    assert 4 + ModularInt(4, 7) == ModularInt(1, 7)


def test_cannot_subtract_different_moduli():
    with pytest.raises(ValueError) as _:
        ModularInt(2, 3) - ModularInt(2, 4)


def test_cannot_subtract_invalid_type():
    with pytest.raises(TypeError) as _:
        ModularInt(2, 3) - 2.0


def test_valid_subtraction():
    assert ModularInt(2, 3) - ModularInt(2, 3) == 0
    assert ModularInt(4, 7) - 5 == ModularInt(6, 7)
    assert 4 - ModularInt(4, 7) == ModularInt(0, 7)


def test_cannot_multiply_different_moduli():
    with pytest.raises(ValueError) as _:
        ModularInt(2, 3) * ModularInt(2, 4)


def test_cannot_multiply_invalid_type():
    with pytest.raises(TypeError) as _:
        ModularInt(2, 3) * 2.0


def test_valid_multiplication():
    assert ModularInt(2, 3) * ModularInt(2, 3) == 1
    assert ModularInt(4, 7) * 5 == ModularInt(6, 7)
    assert 0 * ModularInt(4, 7) == 0


def test_power():
    assert ModularInt(2, 5) ** 0 == 1
    assert ModularInt(2, 5) ** 1 == 2
    assert ModularInt(2, 5) ** 2 == 4
    assert ModularInt(2, 5) ** 3 == 3
    assert ModularInt(2, 5) ** 4 == 1


def test_power_efficiency():
    assert ModularInt(7, 10) ** 10000000000 == 1


def test_zero_has_no_inverse():
    with pytest.raises(ValueError) as _:
        ModularInt(0, 5).inverse()


def test_find_nonexistent_inverse():
    with pytest.raises(ValueError) as _:
        ModularInt(2, 4).inverse()


def test_find_inverse():
    for i in range(1, 97):
        x = ModularInt(i, 97)
        assert x * x.inverse() == 1


def test_illegal_division_with_different_moduli():
    x = ModularInt(1, 4)
    y = ModularInt(1, 3)
    with pytest.raises(ValueError) as _:
        x / y


def test_illegal_division_despite_solution():
    x = ModularInt(10, 15)
    y = ModularInt(5, 15)
    # ModularInt(2, 15) is a solution, but will not be returned
    with pytest.raises(ValueError) as _:
        x / y


def test_legal_division():
    x = ModularInt(2, 7)
    y = ModularInt(5, 7)
    z = ModularInt(6, 7)
    assert x / y == z
    assert x / z == y


def test_legal_division_not_in_field():
    x = ModularInt(2, 6)
    y = ModularInt(5, 6)
    z = ModularInt(4, 6)
    assert x / y == z
    with pytest.raises(ValueError) as _:
        # illegal division despite solution's existence
        x / z == y


def test_repr():
    assert repr(ModularInt(3, 5)) == "ModularInt(3, 5)"


def test_str():
    x = ModularInt(3, 5)
    y = ModularInt(2, 5)
    z = ModularInt(0, 5)
    assert str(x) == "[3]5"
    assert "{} + {} = {}".format(x, y, z) == "[3]5 + [2]5 = [0]5"

# polynomial

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

A class for constructing polynomials over arbitrary rings or fields in python3.

## Examples

    >>> p = Polynomial([3, 2])
    >>> p(0)
    3
    >>> p(1)
    5
    >>> p(2)
    7
    >>> p2 = Polynomial([3, 2]) + Polynomial([4, 3, 1])
    >>> p2
    Polynomial([7, 5, 1])
    >>> p2(1)
    13
    >>> Polynomial([1, 1]) ** 5
    Polynomial([1, 5, 10, 10, 5, 1])

## Tests

Test files are included and can be run with pytest.

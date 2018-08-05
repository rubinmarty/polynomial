class Polynomial:

    """ A class for constructing polynomials over arbitrary
        rings or fields. Because this code is generalized for
        polynomials with coefficients of many algebraic
        types, the implementations may not be optimally efficient
        for calculations involving real-valued polynomials.

        Polynomials are meant to be immutable, and so they can be
        freely aliased without worry. This of course leads to a
        significant performance bottleneck when constructing
        large numbers of polynomials.
    """

    ZERO_DEGREE = None

    def __init__(self, lst):

        if not isinstance(lst, list):
            raise TypeError(
                "Can only construct Polynomial from list, not {}".format(
                    type(lst).__name__
                )
            )

        self.data = lst

        # Remove trailing zeroes
        while self.data and self._leading_coefficient() == 0:
            self.data.pop()

    def __len__(self):
        """ Alias for self.degree() """
        return self.degree()

    def degree(self):
        """ Return the degree of this Polynomial, defined to be the
            largest exponent with a non-zero coefficient. Getting the degree
            of the zero polynomial defaults to throwing an exception,
            but this can overridden with `define_zero_degree`
        """
        if not self.data:
            if self.ZERO_DEGREE is None:
                raise ValueError("Zero Polynomial has undefined degree")
            return self.ZERO_DEGREE
        return len(self.data) - 1

    @staticmethod
    def define_zero_degree(value):
        """ Set the value to be returned when someone calls
            Polynomial([]).degree(). Default degree of the zero
            polynomial is None, which raises a ValueError
        """
        self.ZERO_DEGREE = value

    def __call__(self, value, zero_element=0):
        """ Evaluates the polynomial at the given input value.
            In the event that the polynomial is the zero
            polynomial, zero_element is returned.
        """
        if self.data == []:
            return zero_element

        total = None
        for i, val in enumerate(self.data):
            if total == None:
                total = self.data[i] * value ** i
            else:
                total += self.data[i] * value ** i

        return total

    def __iter__(self):
        """ Iterates over the coefficients, starting from the
            constant term and terminating at the coefficient of
            the greatest non-zero exponent. Includes zero coefficients
            in the iteration.
        """
        return iter(self.data)

    def __eq__(self, other):
        return self.data == other.data

    def __pos__(self):
        return Polynomial(self.data)

    def __neg__(self):
        return Polynomial([-coeff for coeff in self.data])

    def __add__(self, other):

        if not isinstance(other, Polynomial):
            tgt = self.data[:]
            if not tgt:
                return Polynomial([other])
            tgt[0] += other
            return Polynomial(tgt)

        ZERO = Polynomial([])
        if self == ZERO:
            return other
        if other == ZERO:
            return self

        length = max(self.degree(), other.degree()) + 1
        tgt = [None] * length
        for i, v in enumerate(self):
            tgt[i] = v
        for i, v in enumerate(other):
            if tgt[i] is None:
                tgt[i] = v
            else:
                tgt[i] += v

        return Polynomial(tgt)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):

        if not isinstance(other, Polynomial):
            return Polynomial([other * i for i in self.data])

        ZERO = Polynomial([])
        if self == ZERO or other == ZERO:
            return ZERO

        length = self.degree() + other.degree() + 1

        tgt = [None] * length
        for i, v in enumerate(self):
            for j, w in enumerate(other):
                if tgt[i + j] is None:
                    tgt[i + j] = v * w
                else:
                    tgt[i + j] += v * w

        return Polynomial(tgt)

    def _leading_coefficient(self):
        if self.data == []:
            raise ValueError("Zero polynomial has no leading coefficient")
        return self.data[-1]

    def _field_div(self, other):
        p1 = self
        tgt = Polynomial([])
        X = Polynomial([0, 1])
        ZERO = Polynomial([])

        while p1 != ZERO and p1.degree() >= other.degree():
            partial_quotient = p1._leading_coefficient() / other._leading_coefficient()
            if p1.degree() != other.degree():
                partial_quotient *= X ** (p1.degree() - other.degree())
            tgt += partial_quotient
            p1 -= other * partial_quotient

        return tgt

    def _lc_of_one_div(self, other):
        p1 = self
        tgt = Polynomial([])
        X = Polynomial([0, 1])
        ZERO = Polynomial([])

        while p1 != ZERO and p1.degree() >= other.degree():
            partial_quotient = p1._leading_coefficient()
            if p1.degree() != other.degree():
                partial_quotient *= X ** (p1.degree() - other.degree())
            tgt += partial_quotient
            p2 = p1 - other * partial_quotient
            if p2 != ZERO and p2.degree() >= p1.degree():
                raise ValueError
            else:
                p1 = p2

        return tgt

    def __floordiv__(self, other):

        if other == Polynomial([]):
            raise ZeroDivisionError

        try:
            return self._field_div(other)
        except (TypeError, ValueError):
            pass

        try:
            return self._lc_of_one_div(other)
        except ValueError:
            pass

        raise ValueError(
            "Polynomial coefficients not invertible, and leading coefficient of divisor not identity."
        )

    def __mod__(self, other):
        quot = self // other
        return self - (quot * other)

    def __pow__(self, exp):

        if not isinstance(exp, int):
            raise TypeError
        if exp < 1:
            raise ValueError

        # populate exponents that are powers of 2
        saved = {0: 1, 1: self}
        i = 1
        while i * 2 <= exp:
            saved[i * 2] = saved[i] * saved[i]
            i *= 2

        # compute return value
        tgt = 1
        while i > 0:
            if i <= exp:
                exp -= i
                tgt *= saved[i]
            i //= 2

        return tgt

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return self - other

    def __rmul__(self, other):
        return self * other

    """
    def __rfloordiv__(self, other):
        return self // other
    def __rmod__(self, other):
        return self % other
    """

    def __repr__(self):
        return "Polynomial(" + str(self.data) + ")"

    """   
    def __str__(self):
        return str(self.data)
          
        
        
    def plug_in(self, val):
        return sum([val**i * v for i,v in enumerate(self.data)], Polynomial([0]))

    
    def var_term(self, c, x, n):
        if n == 0:
            return "({})".format(repr(c))
        elif n == 1:
            return "({} * {})".format(repr(c), x)
        else:
            return "({} * {}^{})".format(repr(c), x, n)
    
    def str_with_var(self, x):
        tgt = ""
        for n, c in enumerate(self.data):
            if c != 0:
                tgt += self.var_term(c, x, n)
                tgt += " + "
        tgt = tgt[0:len(tgt)-3]
        return tgt    
        
    def str_with_vars(self, xs):
        if len(xs) == 1:
            return self.str_with_var(xs[0])
        else:
            h = xs[0]
            tl = xs[1:]
            save = self.data
            self.data = [v.str_with_vars(tl) for v in self.data]
            tgt = self.str_with_var(h)
            self.data = save
            return tgt
    """


if __name__ == "__main__":
    x = Polynomial([0, 1, 2])
    y = Polynomial([0, 1])

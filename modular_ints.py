class ModularInt():

    """
    """

    def __init__(self, value, modulus):
        if not isinstance(value, int):
            raise TypeError("Value must be of type int, not a {}".format(type(value).__name__))
        if not isinstance(modulus, int):
            raise TypeError("Modulus must be of type int, not a {}".format(type(modulus).__name__))
        if modulus < 1:
            raise ValueError("Modulus must be 1 or greater.")


        self.value = value % modulus
        self.modulus = modulus

    def __eq__(self, other):
        if isinstance(other, ModularInt):
            if self.modulus != other.modulus:
                return False
            else:
                return self.value == other.value
        else:
            return self == ModularInt(other, self.modulus)

    def __neg__(self):
        return ModularInt(-self.value, self.modulus)

    def __add__(self, other):
        if isinstance(other, ModularInt):
            if self.modulus != other.modulus:
                raise ValueError("Can't add two values with different moduli.")
            else:
                return ModularInt(self.value + other.value, self.modulus)

        else:
            return ModularInt(self.value + other, self.modulus)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, ModularInt):
            if self.modulus != other.modulus:
                raise ValueError("Can't multiply two values with different moduli.")
            else:
                return ModularInt(self.value * other.value, self.modulus)

        else:
            return ModularInt(self.value * other, self.modulus)

    def __pow__(self, exp):
        if not isinstance(exp, int):
            raise TypeError("Exponent must be of type int, not {}".format(type(value).__name__))
        if exp < 0:
            raise ValueError("Can't exponentiate to negative power.")

        return ModularInt(self.value.__pow__(exp, self.modulus), self.modulus)


        """
        vals = {0 : ModularInt(1, self.modulus), 1 : self}

        def loop(exp):
            if exp in vals:
                return vals[exp]
            else:
                tgt = loop(exp // 2) * loop(exp - exp // 2)
                vals[exp] = tgt
                return tgt

        return loop(exp)
        """

    def __radd__(self, other):
        return self + other
    def __rsub__(self, other):
        return self - other
    def __rmul__(self, other):
        return self * other


    def __repr__(self):
        return "ModularInt({}, {})".format(self.value, self.modulus)

    def __str__(self):
        return "[{}]{}".format(self.value, self.modulus)

    def inverse(self):
        # Extended Euclidean Algorithm for computing GCD and modular inverses
        a, b = self.modulus, self.value
        x0, x1 = 1, 0
        while a != 0:
            (q, a), b = divmod(b, a), a
            x0, x1 = x1, x0 - q * x1
        if b != 1:
            raise ValueError("{} is not invertible modulo {}.".format(self.value, self.modulus))
        return x0
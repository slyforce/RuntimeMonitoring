

class BooleanExpression:

    def simplify(self):
        return self

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        h = 0
        for k,v in self.__dict__.items():
            h ^= hash((k, v))
        return h


class FalseBooleanExpression(BooleanExpression):
    def eval(self):
        return False

    def __str__(self):
        return "FALSE"


class TrueBooleanExpression(BooleanExpression):
    def eval(self):
        return True

    def __str__(self):
        return "TRUE"


class VarExpression(BooleanExpression):
    def __init__(self, var: int):
        self.var = var

    def __str__(self):
        return "VAR {}".format(self.var)


class NegVarExpression(BooleanExpression):
    def __init__(self, var: int):
        self.var = var

    def __str__(self):
        return "NOT VAR {}".format(self.var)


class NegationBooleanExpression(BooleanExpression):
    def __init__(self,
                 formula: BooleanExpression):
        self.formula = formula

    def __str__(self):
        return "NOT {}".format(str(self.formula))

    def simplify(self):
        if isinstance(self.formula, TrueBooleanExpression):
            return FalseBooleanExpression()
        elif isinstance(self.formula, FalseBooleanExpression):
            return TrueBooleanExpression()

        return self

class ConjunctionBooleanExpression(BooleanExpression):
    def __init__(self,
                 formula_1: BooleanExpression,
                 formula_2: BooleanExpression):
        self.formula_1 = formula_1
        self.formula_2 = formula_2

    def __str__(self):
        return "{} OR {}".format(str(self.formula_1),
                                 str(self.formula_2))

    def simplify(self):
        if isinstance(self.formula_1, FalseBooleanExpression):
            return self.formula_2
        elif isinstance(self.formula_2, FalseBooleanExpression):
            return self.formula_1

        if isinstance(self.formula_1, TrueBooleanExpression) or isinstance(self.formula_2, TrueBooleanExpression):
            return TrueBooleanExpression()

        return self


class DisjunctionBooleanExpression(BooleanExpression):
    def __init__(self,
                 formula_1: BooleanExpression,
                 formula_2: BooleanExpression):
        self.formula_1 = formula_1
        self.formula_2 = formula_2

    def __str__(self):
        return "{} AND {}".format(str(self.formula_1),
                                  str(self.formula_2))

    def simplify(self):
        if isinstance(self.formula_1, TrueBooleanExpression):
            return self.formula_2
        elif isinstance(self.formula_2, TrueBooleanExpression):
            return self.formula_1

        if isinstance(self.formula_1, FalseBooleanExpression) or isinstance(self.formula_2, FalseBooleanExpression):
            return FalseBooleanExpression()

        return self

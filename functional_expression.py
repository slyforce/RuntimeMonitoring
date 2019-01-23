from boolean_expression import BooleanExpression


class FunctionalExpression:
    pass


class NowFormulaExpression(FunctionalExpression):
    def __init__(self,
                 boolean_expr: BooleanExpression):
        self.bool_expr = boolean_expr

    def __str__(self):
        return "NOW {}".format(str(self.bool_expr))


class LaterFormulaExpression(FunctionalExpression):
    def __init__(self,
                 boolean_expr):  # lambda function int -> bool
        self.bool_expr = boolean_expr

    def __str__(self):
        return "LATER t -> {}".format(self.bool_expr(0))


class NegFunctionalExpression(FunctionalExpression):
    def __init__(self,
                 formula: FunctionalExpression):
        self.formula = formula

    def __str__(self):
        return "NOT {}".format(str(self.formula))


class ConjunctionFunctionalExpression(FunctionalExpression):
    def __init__(self,
                 formula_1: FunctionalExpression,
                 formula_2: FunctionalExpression):
        self.formula_1 = formula_1
        self.formula_2 = formula_2

    def __str__(self):
        return "{} OR {}".format(str(self.formula_1),
                                 str(self.formula_2))


class DisjunctionFunctionalExpression(FunctionalExpression):
    def __init__(self,
                 formula_1: FunctionalExpression,
                 formula_2: FunctionalExpression):
        self.formula_1 = formula_1
        self.formula_2 = formula_2

    def __str__(self):
        return "{} AND {}".format(str(self.formula_1),
                                  str(self.formula_2))

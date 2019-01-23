import formula as F
import boolean_expression as BE
import functional_expression as FE

import test_cases

from typing import List, Tuple, Set

class Monitor:
    def __init__(self, formula: F.Formula):
        self.formula = formula
        self._reset()

    def _reset(self):
        self.history = set()
        self.subformulae = []
        self.current = []
        self.previous = []
        self.current_timestamp = -1
        self.current_timestamp_offset = 0
        self.current_character = ''
        self._create_arrays()

    def _create_arrays(self):
        self._create_array_recursion_helper(self.formula)

        # reverse the list of sub-formulae as they have been inserted in the reverse order
        self.subformulae = list(reversed(self.subformulae))

        self.N = len(self.subformulae)

    def _create_array_recursion_helper(self,
                                       formula: F.Formula):

        # initialize arrays with expressions which evaluate to False
        # also keep track of the formulae

        def _add_formula(self, formula):
            self.subformulae.append(formula)
            self.previous.append(BE.FalseBooleanExpression())
            self.current.append(FE.NowFormulaExpression(BE.FalseBooleanExpression()))

        _add_formula(self, formula)

        # add all possible intervals as sub-formulae to ensure that they are evaluated first
        if (isinstance(formula, F.Until) or isinstance(formula, F.Since)
                or isinstance(formula, F.Next) or isinstance(formula, F.Previous)):

            current_formula = formula
            while not current_formula.interval.is_empty():
                current_formula = current_formula.copy()
                current_formula.interval.decrement()
                _add_formula(self, current_formula)

        # recursion step: add all sub-formulae to the array
        if isinstance(formula, F.Negation) or isinstance(formula, F.Next) or isinstance(formula, F.Previous):
            self._create_array_recursion_helper(formula.formula)
        elif isinstance(formula, F.Until) or isinstance(formula, F.Since) or isinstance(formula, F.Conjunction):
            self._create_array_recursion_helper(formula.formula1)
            self._create_array_recursion_helper(formula.formula2)

    def substitute_boolean_expression(self, expr: BE.BooleanExpression) -> BE.BooleanExpression:
        out = None
        if isinstance(expr, BE.FalseBooleanExpression) or isinstance(expr, BE.TrueBooleanExpression):
            out = expr
        elif isinstance(expr, BE.VarExpression):
            out = self.previous[expr.var]
        elif isinstance(expr, BE.NegVarExpression):
            out = BE.NegationBooleanExpression(self.previous[expr.var])
        elif isinstance(expr, BE.DisjunctionBooleanExpression):
            out = BE.DisjunctionBooleanExpression(formula_1=self.substitute_boolean_expression(expr.formula_1),
                                                  formula_2=self.substitute_boolean_expression(expr.formula_2))

        elif isinstance(expr, BE.ConjunctionBooleanExpression):
            out = BE.ConjunctionBooleanExpression(formula_1=self.substitute_boolean_expression(expr.formula_1),
                                                  formula_2=self.substitute_boolean_expression(expr.formula_2))

        return out.simplify()

    def substitute_functional_expression(self, expr: BE.BooleanExpression) -> FE.FunctionalExpression:
        if isinstance(expr, BE.FalseBooleanExpression) or isinstance(expr, BE.TrueBooleanExpression):
            return FE.NowFormulaExpression(expr)
        elif isinstance(expr, BE.VarExpression):
            return self.current[expr.var]
        elif isinstance(expr, BE.NegVarExpression):
            return FE.NegFunctionalExpression(formula=self.current[expr.var])
        elif isinstance(expr, BE.DisjunctionBooleanExpression):
            return FE.DisjunctionFunctionalExpression(formula_1=self.substitute_functional_expression(self.current[self.get_formula_index(expr.formula_1)]),
                                                      formula_2=self.substitute_functional_expression(self.current[self.get_formula_index(expr.formula_2)]))

        elif isinstance(expr, BE.ConjunctionBooleanExpression):
            return FE.ConjunctionFunctionalExpression(formula_1=self.substitute_functional_expression(self.current[self.get_formula_index(expr.formula_1)]),
                                                      formula_2=self.substitute_functional_expression(self.current[self.get_formula_index(expr.formula_2)]))


    def filter_verdicts(self, history):
        """
        In-place removal of verdicts which are either
        1. evaluated to true or false expressions or
        2. have an equivalent boolean expression to other elements in the history
        """
        self._filter_true_or_false_verdicts(history)
        self._filter_equivalent_verdicts(history)

    def _filter_equivalent_verdicts(self, history: Set[Tuple[Tuple[int, int], BE.BooleanExpression]]):
        """
        Remove entries from the history with the same boolean expression, but with different timestamps.
        """
        elements_to_remove = set()
        for entry1 in history:
            ((timestamp1, offset1), b_expr1) = entry1

            for entry2 in history:
                ((timestamp2, offset2), b_expr2) = entry2

                # skip entries if they do not have the same boolean expression
                if entry1 == entry2 or b_expr1 != b_expr2:
                    continue

                # remove entries with a larger timestamp (and the same boolean expression)
                if (timestamp1 == timestamp2 and offset1 < offset2) or timestamp1 < timestamp2:
                    elements_to_remove.add(entry2)

        for entry in elements_to_remove:
            history.remove(entry)

    def _filter_true_or_false_verdicts(self, history: Set[Tuple[Tuple[int, int], BE.BooleanExpression]]):
        """
        Remove entries from the history with a boolean expression that is already evaluated to either True or False.
        """
        elements_to_remove = set()
        for entry in history:
            (_, b_expr) = entry
            if b_expr == BE.TrueBooleanExpression() or b_expr == BE.FalseBooleanExpression():
                elements_to_remove.add(entry)
        for entry in elements_to_remove:
            history.remove(entry)

    def eval(self, f_expr: FE.FunctionalExpression, delta_t: int) -> BE.BooleanExpression:
        out = None
        if isinstance(f_expr, FE.NowFormulaExpression):
            out = f_expr.bool_expr
        elif isinstance(f_expr, FE.LaterFormulaExpression):
            out = f_expr.bool_expr(delta_t)
        elif isinstance(f_expr, FE.NegFunctionalExpression):
            out = BE.NegationBooleanExpression(self.eval(f_expr.formula, delta_t))
        elif isinstance(f_expr, FE.DisjunctionFunctionalExpression):
            out = BE.DisjunctionBooleanExpression(formula_1=self.eval(f_expr.formula_1, delta_t),
                                                  formula_2=self.eval(f_expr.formula_2, delta_t))

        elif isinstance(f_expr, FE.ConjunctionFunctionalExpression):
            out = BE.ConjunctionBooleanExpression(formula_1=self.eval(f_expr.formula_1, delta_t),
                                                  formula_2=self.eval(f_expr.formula_2, delta_t))

        return out.simplify()

    def get_formula_index(self, formula: F.Formula) -> int:
        """
        TODO: Access to sub-formulae currently needs to iterate over list -> use pointers to sub-formualae
        """
        assert formula in self.subformulae, "Array contents: {} \n Formula {}".format(self.subformulae, formula)
        return self.subformulae.index(formula)

    def progress(self, formula_idx: int, delta_t: int, character: str) -> FE.FunctionalExpression:
        formula = self.subformulae[formula_idx]

        if isinstance(formula, F.Proposition):
            if character == formula.character:
                return FE.NowFormulaExpression(BE.TrueBooleanExpression())
            else:
                return FE.NowFormulaExpression(BE.FalseBooleanExpression())

        elif isinstance(formula, F.Negation):
            return FE.NegFunctionalExpression(formula=self.current[self.get_formula_index(formula.formula)])

        elif isinstance(formula, F.Conjunction):
            return FE.ConjunctionFunctionalExpression(formula_1=self.current[self.get_formula_index(formula.formula1)],
                                                      formula_2=self.current[self.get_formula_index(formula.formula2)])

        elif isinstance(formula, F.Previous):

            # NOTE: simplified expansion of previous case
            if formula.interval.is_in_interval(delta_t):
                return self.substitute_functional_expression(self.previous[self.get_formula_index(formula.formula)])
            else:
                return FE.NowFormulaExpression(BE.FalseBooleanExpression())

        elif isinstance(formula, F.Next):
            return FE.LaterFormulaExpression(boolean_expr=lambda x: BE.VarExpression(self.get_formula_index(formula.formula))
                                                                    if formula.interval.is_in_interval(x)
                                                                    else BE.FalseBooleanExpression())

        elif isinstance(formula, F.Since):
            return FE.ConjunctionFunctionalExpression(formula_1=FE.NowFormulaExpression(BE.FalseBooleanExpression())
                                                        if formula.interval.begin == 0
                                                        else self.current[self.get_formula_index(formula.formula2)],
                                                      formula_2=FE.NowFormulaExpression(BE.FalseBooleanExpression())
                                                        if delta_t <= formula.interval.end
                                                        else FE.ConjunctionFunctionalExpression(formula_1=self.current[self.get_formula_index(formula.formula1)],
                                                                                                formula_2=self.substitute_functional_expression(self.previous[formula_idx - delta_t]))
                                                      )
        elif isinstance(formula, F.Until):
            return FE.ConjunctionFunctionalExpression(formula_1=FE.NowFormulaExpression(BE.FalseBooleanExpression())
                                                        if formula.interval.begin == 0
                                                        else self.current[self.get_formula_index(formula.formula2)],
                                                      formula_2=FE.LaterFormulaExpression(lambda x: BE.DisjunctionBooleanExpression(formula_1=self.eval(self.current[self.get_formula_index(formula.formula1)], x),
                                                                                                                                    formula_2=BE.VarExpression(formula_idx - x)
                                                                                                                                    if formula.interval.is_in_interval(x) else BE.FalseBooleanExpression())
                                                                                          )
                                                      )

    def step(self, timestamp: int, character: str):
        delta_t = timestamp - self.current_timestamp
        for k in range(self.N):
            self.previous[k] = self.eval(self.current[k], delta_t)

        filtering_input = set()
        filtering_input.add(((self.current_timestamp, self.current_timestamp_offset), self.previous[-1]))
        for time_info, c in self.history:
            filtering_input.add((time_info, self.substitute_boolean_expression(c)))
        self.filter_verdicts(filtering_input)
        self.history = filtering_input

        self.current_timestamp = timestamp
        self.current_character = character
        if delta_t > 0:
            self.current_timestamp_offset = 0
        else:
            self.current_timestamp_offset += 1

        for k in range(self.N):
            self.current[k] = self.progress(k, delta_t, character)

    def _debug(self):

        print("Timestamp/Offset: {}/{}".format(self.current_timestamp, self.current_timestamp_offset))
        print("Character: {}".format(self.current_character))

        print("History:")
        for entry in self.history:
            time_information, b_expr = entry
            print(time_information, str(b_expr))

        print("Current formulae:")
        for k in range(self.N):
            print(str(self.subformulae[k]))

        print("Previous array:")
        for k in range(self.N):
            print(str(self.previous[k]))

        print("Current array:")
        for k in range(self.N):
            print(str(self.current[k]))

        print("")

    def run(self, pattern: List[Tuple[int, str]]) -> bool:
        self._reset()

        for timestamp, char in pattern:
            self._debug()
            self.step(timestamp, char)

        self._debug()
        return True


def main():
    pattern = [(1, 'a'), (2,'a'), (2,'a'), (3,'b')]

    print("Running UNTIL test")
    monitor = Monitor(test_cases.until())
    monitor.run(pattern)

    return
    print("Running SINCE test")
    monitor = Monitor(test_cases.since())
    monitor.run(pattern)

if __name__ == '__main__':
    main()
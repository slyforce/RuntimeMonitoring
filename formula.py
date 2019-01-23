import copy


class Formula:
    def eval(self, character):
        raise NotImplementedError

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return ""

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


class Interval:
    def __init__(self, begin: int, end: int):
        self.begin = begin
        self.end = end

    def decrement(self):
        self.begin = max(0, self.begin - 1)
        self.end = max(0, self.end - 1)

    def is_empty(self):
        return self.begin == self.end == 0

    def is_in_interval(self, value: int):
        return self.begin <= value <= self.end

    def __str__(self):
        return "[{}-{}]".format(self.begin, self.end)

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


class Proposition(Formula):
    def __init__(self, character):
        self.character = character

    def __str__(self):
        return "x={}".format(self.character)


class Negation(Formula):
    def __init__(self, formula: Formula):
        self.formula = formula

    def __str__(self):
        return "NOT {}".format(str(self.formula))


class Conjunction(Formula):
    def __init__(self,
                 formula_1: Formula,
                 formula_2: Formula):
        self.formula1 = formula_1
        self.formula2 = formula_2

    def __str__(self):
        return "{} OR {}".format(str(self.formula1),
                                 str(self.formula2))


class Previous(Formula):
    def __init__(self,
                 formula: Formula,
                 interval: Interval):
        self.formula = formula
        self.interval = interval

    def __str__(self):
        return "PREVIOUS {} {}".format(str(self.formula),
                                       str(self.interval))



class Next(Formula):
    def __init__(self,
                 formula: Formula,
                 interval: Interval):
        self.formula = formula
        self.interval = interval

    def __str__(self):
        return "NEXT {} {}".format(str(self.formula),
                                   str(self.interval))


class Since(Formula):
    def __init__(self,
                 formula1: Formula,
                 formula2: Formula,
                 interval: Interval):
        self.formula1 = formula1
        self.formula2 = formula2
        self.interval = interval

    def __str__(self):
        return "SINCE {} {} {}".format(str(self.formula1),
                                       str(self.interval),
                                       str(self.formula2))



class Until(Formula):
    def __init__(self,
                 formula1: Formula,
                 formula2: Formula,
                 interval: Interval):
        self.formula1 = formula1
        self.formula2 = formula2
        self.interval = interval

    def __str__(self):
        return "UNTIL {} {} {}".format(str(self.formula1),
                                       str(self.interval),
                                       str(self.formula2))

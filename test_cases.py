import formula as F

def pattern_aaabb():
    return [(1, 'a'), (2,'a'), (2,'a'), (3,'b'), (4, 'b')]


def conjunction():
    return F.Conjunction(formula_1=F.Proposition(character='a'),
                         formula_2=F.Proposition(character='b'))


def until():
    return F.Until(formula1=F.Proposition(character='a'),
                   formula2=F.Proposition(character='b'),
                   interval=F.Interval(0, 1))


def since():
    return F.Since(formula1=F.Proposition(character='a'),
                   formula2=F.Proposition(character='b'),
                   interval=F.Interval(0, 1))
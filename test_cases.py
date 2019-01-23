import formula as F


def until():
    return F.Until(formula1=F.Proposition(character='a'),
                   formula2=F.Proposition(character='b'),
                   interval=F.Interval(0, 1))


def since():
    return F.Since(formula1=F.Proposition(character='a'),
                   formula2=F.Proposition(character='b'),
                   interval=F.Interval(0, 1))
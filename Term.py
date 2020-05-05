class Term(object):

    def __init__(self, coefficient, exponent):
        self.coefficient = coefficient
        self.exponent = exponent

    def getCoefficient(self):
        return self.coefficient

    def getExponent(self):
        return self.exponent

    def evaluate(self, x):
        return self.coefficient * (x ** self.exponent)

    def __str__(self):
        if (self.exponent == 1):
            return str(self.coefficient) + 'x'
        elif (self.exponent == 0):
            return str(self.coefficient)
        else:
            return str(self.coefficient) + 'x^' + str(self.exponent) 

    def __gt__(self, other):
        return self.getExponent() < other.getExponent()

    def __lt__(self, other):
        return self.getExponent() > other.getExponent()


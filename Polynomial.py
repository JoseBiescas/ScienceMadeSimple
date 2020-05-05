from Term import Term

class Polynomial:

    def __init__(self, polynomial):
        self.mylist = list()
        self.polynomial = ""
        self.verifyPolynomial(polynomial)
        self.scanPolynomial(polynomial)

    def verifyPolynomial(self, polynomial):
        for i in range(0, len(polynomial)):
            char = polynomial[i]
            if char != 'x' and char != '^' and char != '.' and char != '+' and char != '-' and char.isdigit() == False:
                raise Exception("Invalid character " + char + " at position " + i + ", make sure that the"
						+ " polynomial is in term of x's only and well written.")
            elif i < len(polynomial) - 1 and char.isdigit() == False and char == polynomial[i+1]:
                raise Exception('"' + polynomial  + '"' + " doesn't seem to be a valid polynomial. Verify that no characters are repeated.")

    def scanPolynomial(self, polynomial):
        start = 0
        for i in range (0, len(polynomial)):
            if(i > 0 and (polynomial[i] == '+' or polynomial[i] == '-') and (polynomial[i-1] == '+' or polynomial[i-1] == '-') == False):
                term = polynomial[start:i]
                self.addTerm(term)
                start = i
        if start != len(polynomial):
            self.addTerm(polynomial[start:])

        self.mylist.sort()
        self.polynomial = self.findCommonTerms(self.mylist)

    def addTerm(self, term):
        coefficient = 0.0
        exponent = 0

        if '+' in term and '-' in term:
            term = term.replace('+', "")

        if 'x' not in term:
            coefficient = float(term)
            exponent = 0

        elif '^' not in term:
            try:
                coefficient = float(term[0:term.index('x')])
            except:
                coefficient = 1
            exponent = 1

        else:
            try:
                coefficient = float(term[0:term.index('x')])
            except:
                coefficient = 1
            exponent = int(term[term.index('^') + 1:])

        if coefficient != 0:
            self.mylist.append(Term(coefficient, exponent))

    def findCommonTerms(self, l):
        polynomial = ""
        for i in range (0, len(l)):
            j = i + 1
            while(i < len(l) - 1 and l[i].getExponent() == l[j].getExponent()):
                modifiedTerm = Term(l[i].getCoefficient() + l[j].getCoefficient(), l[i].getExponent())
                l[i] = modifiedTerm
                l.remove(j)
			
            if l[i] != l[0]:
                polynomial += '+'
            polynomial += str(l[i])

            if(len(polynomial) != 0):
                return polynomial
            else:
                return "0.00"

    def getPolynomialSize(self):
        return len(self.mylist)
		
    def indefiniteIntegral(self):
        integral = ""
        for term in self.mylist:
            n = int(term.getExponent() + 1)
            integratedTerm = Term(term.getCoefficient()/n, n)
            if term != self.mylist[0]:
                integral += '+'
            integral += str(integratedTerm)

        integral += "+C"
        
        return integral


    def derivative(self):
        derivative = ""
        for term in self.mylist:
            if term.getExponent() != 0:
                derivedTerm = Term(term.getCoefficient()*term.getExponent(), term.getExponent()-1)
                if term != self.mylist[0]:
                    derivative += "+"
                derivative += str(derivedTerm)
			
		
        return derivative
	
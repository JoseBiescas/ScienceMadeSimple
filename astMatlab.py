import operator
from types import LambdaType

class MAIN:
    def __init__(self, childs=None):
        if childs is None:
            childs = []
        self.childs = childs
    
    def __len__(self):
        return len(self.childs)
    
    def __repr__(self):
        return 'Main {0}'.format(self.childs)

    def __iter__(self):
        return iter(self.childs)
    
    def evaluate(self):
        returnlist = []
        for n in self:
            result = n

            if result is not None:
                returnlist.append(result)
        
        return returnlist

class BaseExpression:
    def evaluate(self):
        raise NotImplementedError()

class BINOP(BaseExpression):
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        # '%': operator.mod,
        '^': operator.pow
    }
    def __init__(self, operation, num1, num2):
        self.operation = operation
        self.num1 = num1
        self.num2 = num2

    def __repr__(self):
        return 'BinOP : {0} {1} {2}'.format(self.num1, self.operation, self.num2)

    def evaluate(self):
        op = self.operations[self.operation]
        # num1 = self.num1.evaluate()
        # num2 = self.num2.evaluate()

        return op(self.num1, self.num2)

class BOOL(BaseExpression):
    operations = {
        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
        '&': operator.and_,
        '|': operator.or_,
        '!=': operator.ne,
    }

    def __init__(self, operation, num1, num2):
        self.operation = operation
        self.num1 = num1
        self.num2 = num2

    
    def __repr__(self):
        return 'Bool : {0} {1} {2}'.format(self.num1, self.operation, self.num2)

    def evaluate(self):
        op = self.operations[self.operation]
        # num1 = self.num1.evaluate()
        # num2 = self.num2.evaluate()

        return op(self.num1, self.num2)


class UNARY(BaseExpression):
    operators = {
        '-' : operator.neg
    }
    def __init__(self, operation, expression: BaseExpression):
        self.operation = operation
        self.expression = expression
    
    def __repr__(self):
        return 'UNARY : {0} {1}'.format(self.operation, self.expression)
    
    def evaluate(self):
        return self.operators[self.operation](self.expression)
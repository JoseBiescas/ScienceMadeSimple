import ply.yacc as yacc
import astMatlab as ast
import itertools
import math
import sys

from lexer import Lexer
from Polynomial import Polynomial

IDS = {}
IDList = {}

GRAVITY = 9.80665
PLANCK = 6.62607004 * (10**-34)
PI = 3.141592653589793
EULIER = 2.718281828459045235360

class Parser():
    m = Lexer()
    m.build()
    tokens = m.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', '^'),
        ('right', 'UMINUS'),
    )

    def p_program(self, p):
        '''program : expression
                   | expression program'''
        p[0] = ast.MAIN([p[1]]).evaluate()
        #print(p[0])

    # Done this way so there is precedence clearly stated
    def p_expression_binop(self, p):
        '''expression : expression '+' expression %prec '+'
            | expression '-' expression %prec '-'
            | expression '*' expression %prec '*'
            | expression '/' expression %prec '/'
            | expression '^' expression %prec '^' '''
        p[0] = ast.BINOP(p[2], p[1], p[3]).evaluate()
    
    def p_expression_boolean(self,p): 
        '''expression : expression '|' expression
                      | expression LTOE expression
                      | expression GTOE expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression '&' expression
                      | expression NOTEQ expression'''
        p[0] = ast.BOOL(p[2], p[1], p[3]).evaluate()

    def p_expression_unary(self, p):
        '''expression : '-' expression %prec UMINUS'''
        p[0] = ast.UNARY(p[1], p[2]).evaluate()

    def p_expression_par(self, p):
        '''expression : '(' expression ')' '''
        p[0] = p[2]

    def p_expression_assign(self, p):
        '''expression : ID '=' expression'''
        p[0] = ast.MAIN([p[1], p[2], p[3]])
        IDS[p[1]] = p[3]

    # def p_expression_for_loop(self, p):
    #     '''expression : FOR identifier FROM INT TO INT ':' expression'''

    # def p_expression_for_loop(self, p):
    #     '''expression : FOR identifier AT List'''
        
    def p_expression_ques(self, p):
        '''expression : expression ',' expression '?' expression'''
        if p[5]:
            p[0] = p[1]
        else:
            p[0] = p[3]

    def p_expression(self, p):
        '''expression : TERM'''
        p[0] = p[1]

    def p_term(self, p):
        '''
        TERM : NUMBER
             | BOOLEAN
             | STRING
             | empty
             | identifier
             | sciences
             | list
             | show
             '''
        p[0] = p[1]

    def p_list(self, p):
        '''
        list : '[' EXPList ']'
             | '[' IDList ']'
        '''

        p[0] = p[2]

    def p_expList(self, p):
        '''
        EXPList : expression ',' EXPList
                | expression
        '''

        p[0] = list()

        self.removeNestings(p, p[0])

    def removeNestings(self, l, o): 
        for i in l: 
            if type(i) == list: 
                self.removeNestings(i, o) 
            elif type(i) == int: 
                o.append(i) 

    def p_IDList(self, p):
        '''
        IDList : identifier
               | identifier ',' IDList
        '''

        p[0] = list()

        self.removeNestings(p, p[0])

    def p_IDENTIFIER(self, p):
        '''
        identifier : ID
        '''
        p[0] = IDS.get(p[1], p[1])

    def p_empty(self, p):
        'empty :'
        pass

    def p_show(self, p):
        '''
        show : SHOW '(' expression ')'
        '''
        print(p[3])

    def p_CONSTANTS(self, p):
        '''
        CONSTANT : GRAVITY
                 | PLANCK
                 | PI
                 | EULIER
        '''

        if p[1] == 'gravity':
            p[0] = GRAVITY
        elif p[1] == 'planck':
            p[0] = PLANCK
        elif p[1] == 'pi':
            p[0] = PI
        elif p[1] == 'eulier':
            p[0] = EULIER

    def p_BOOLEAN(self, p):
        '''
        BOOLEAN : TRUE
                | FALSE
                '''

        p[0] = p[1]

    def p_NUMBER(self, p):
        '''
        NUMBER : FLOAT
               | INT
               | CONSTANT
               '''
        p[0] = p[1]

    def p_SCIENCES(self, p):
        '''
        sciences : physics
                 | chemistry
                 | math
                 | EPERCENT '(' NUMBER ',' NUMBER ')'
        '''

        # EPERCENT PARAMETERS: approximate value, exact value
        # FORMULA = (|aprox - exact|/exact) * 100

        if(p[1] == 'epercent'):
            p[0] = (abs(p[3] - p[5])/p[5]) * 100
        else:
            p[0] = p[1]

    def p_PHYSICS(self, p):
        '''
        physics : POSITION '(' TERM ',' TERM ',' TERM ',' TERM ')'
                | INITIALVELOCITY '(' TERM ',' TERM ',' TERM ')'
                | FINALVELOCITY '(' TERM ',' TERM ',' TERM ',' TERM ')'
                | AVERAGEVELOCITY '(' TERM ',' TERM ',' TERM ')'
                | VELOCITYX '(' TERM ',' TERM ')'
                | VELOCITYY '(' TERM ',' TERM ')'
                | ACCELERATION '(' TERM ',' TERM ',' TERM ')'
                | POTENTIALENERGY '(' TERM ',' TERM ')'
                | KINETICENERGY '(' TERM ',' TERM ')'
        '''

    # POSITION PARAMETERS: acceleration, time, initial velocity and initial position
    # FORMULA = 0.5 * a * t^2 + v0*t + initial position

        if (p[1] == 'position'):
            p[0] = 0.5 * p[3] * p[5]**2 + p[7]*p[5] + p[9]

    # INITIAL VELOCITY PARAMETERS: final velocity, acceleration, displacement
    # FORMULA: sqrt(vF^2 - 2*a*displacement)

        elif (p[1] == 'initialVelocity'):               
            p[0] = math.sqrt(p[3]**2 - 2 * p[5] * p[7])

    # FINAL VELOCITY:  initial velocity, acceleration, (displacement or time), boolean
    # FORMULA 1: sqrt(v0^2 + 2*a*displacement), if boolean is true
    # FORMULA 2: v0 + a*t, if boolean is false

        elif (p[1] == 'finalVelocity'):
            if(p[9] == True):
                p[0] = math.sqrt(p[3]**2 + 2 * p[5] * p[7])
            else:
                p[0] = p[3] + p[5] * p[7]

    # AVERAGE VELOCITY PARAMETERS: initial position, final position, time
    # FORMULA = (xF - x0)/t

        elif (p[1] == 'averageVelocity'):
            p[0] = (p[3]-p[5])/p[7]

    # VELOCITY IN X PARAMETERS: the overall velocity
    # FORMULA: v*cos(theta)

        elif (p[1] == 'velocityY'):
            p[0] == p[3] * math.cos(p[5])

    # VELOCITY IN Y PARAMETERS: the overall velocity
    # FORMULA: v*sin(theta)

        elif (p[1] == 'velocityX'):
            p[0] == p[3] * math.sin(p[5])

    # ACCELERATION PARAMETERS: initial velocity, final velocity, time
    # FORMULA: (vF - v0)/t

        elif (p[1] == 'acceleration'):
            p[0] = (p[3]-p[5])/p[7]

    # POTENTIAL ENERGY PARAMETERS: mass, vertical height
    # FORMULA: m * G * h

        elif (p[1] == 'potentialEnergy'):
            p[0] == p[3] * 9.80665 * p[5]

    # KINETIC ENERGY PARAMETERS: mass, velocity
    # FORMULA: 0.5 * m * v^2

        elif (p[1] == 'kineticEnergy'):
            p[0] == 0.5 * p[3] * p[5]

    def p_CHEMISTRY(self, p):
        '''
        chemistry : BROGLIE '(' TERM ',' TERM ')'
                  | COULOMB '(' TERM ',' TERM ',' TERM ',' TERM ')'
                  | HEATTRANSFER '(' TERM ',' TERM ',' TERM ')'
                  | BFP '(' TERM ',' TERM ',' TERM ')'
        '''
        #de Broglie Parameters: planck's constant, mass, velocity
        #FORMULA : planck / (m*v)
        if p[1] == "broglie":
            p[0] = PLANCK / (p[3] *p[5])

        #COULOMBS LAW PARAMETERS: charge1, charge2, distance, coulombs law constant
        # (depends on the medium where the charges are found)
        #FORMULA : F = (coulombs law constant * charge1 * charge2) / distance
        if p[1] == 'coulomb':
            p[0] = (p[3] * p[5] * p[9]) / p[7]
        
        # HEAT TRANSFER PARAMETERS: mass, specific heat, change in temperature
        #FORMULA: q = mass * specific heat * change in temperature
        if p[1] == 'heatTransfer':
            p[0] = p[3] *p[5] *p[7]

        #BOILING POINT ELEVATION PARAMETERS: Molal boiling point constant, molality, Van't Hoff factor
        #or FREEZING POINT DEPRESSION PARAMETERS: Molal freezing point constant, molality, Van't Hoff factor
        #FORMULA : molal(freezing or boiling point) * molality * van't hoff factor
        if p[1] == 'bfp':
            p[0] = p[3] * p[5] * p[7]

    def p_MATH(self, p):
        '''
        math : INTEGRALAPPROXIMATION '(' TERM ',' TERM ',' TERM  ',' TERM ')' 
             | INTEGRAL '(' TERM ')'
             | DERIVATIVE '(' TERM ')'
             | DOTPRODUCT '(' TERM ',' TERM ')'
             | CROSSPRODUCT '(' TERM ',' TERM ')'
             | SUMMATION '(' TERM ',' TERM ',' TERM ')'
        '''

        if(p[1] == 'integralApproximation'):
            h = float(p[9]-p[7])/p[5]
            result = 0
            
            if('^' in p[3]):
                p[3] = p[3].replace('^', '**')

            if('e' in p[3]):
                p[3] = p[3].replace('e', '2.718281828459045')

            if('pi' in p[3]):
                p[3] = p[3].replace('pi', '3.141592653589793')

            for i in range(p[5]):
                f = p[3]

                if 'cos(x)' in f:
                    f = f.replace('cos(x)', str(math.cos((p[7] + h/2.0) + i*h)))
                if 'sin(x)' in f:
                    f = f.replace('sin(x)', str(math.sin((p[7] + h/2.0) + i*h)))

                f = f.replace('x', str((p[7] + h/2.0) + i*h))

                result += eval(f)
            result *= h
            p[0] = result

        #PARAMETER: A string with the polynomial to integrate
        if(p[1] == 'integral'):
            p[0] = Polynomial(p[3]).indefiniteIntegral()

        #PARAMETER: A string with the polynomial to derivate
        if(p[1] == 'derivative'):
            p[0] = Polynomial(p[3]).derivative()
        
        #Accepted parameters are two vectors with the same length
        if(p[1] == 'dotProduct' and len(p[3]) == len(p[5]) and len(p[5])==3):
            p[0] = 0
            for i in range (0, len(p[5])):
                p[0] += p[3][i] * p[5][i]

        #Accepted parameters are two vectors with the same length
        if(p[1] == 'crossProduct' and len(p[3]) == len(p[5]) and len(p[5])==3):
            p[0] = list()

            p[0].append(p[3][1] * p[5][2] - p[3][2] * p[5][1])
            p[0].append(p[3][2] * p[5][0] - p[3][0] * p[5][2])
            p[0].append(p[3][0] * p[5][1] - p[3][1] * p[5][0])

        #PARAMATERS: A string with the equation and two numbers with the ranges of the summation
        if(p[1] == 'summation'):
            sum = 0
            if('^' in p[3]):
                p[3] = p[3].replace('^', '**')

            for n in range (p[5],p[7] + 1):
                f = p[3].replace('x', str(n))

                if 'cos(x)' in f:
                    f = f.replace('cos(x)', str(math.cos((p[7] + h/2.0) + i*h)))
                if 'sin(x)' in f:
                    f = f.replace('sin(x)', str(math.sin((p[7] + h/2.0) + i*h)))

                sum += eval(f)

            p[0] = sum

    def p_error(self, p):
        print("Syntax error in input!")

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        print("Built succesfully")

    def test_doc(self, file):
        while True:
            try:
                f = open(file, "r")
                doc = ''
            except EOFError:
                break
            if not f:
                continue
            for w in f:
                doc += w
            f.close()
            print(doc)
            self.parser.parse(doc)
            print("Parse finished.")
            break

    def test_str(self):
        while True:
            try:
                s = input("parse > ")
            except EOFError:
                break
            if not s:
                continue
            self.parser.parse(s, debug=False)
            print("Parse finished.")

if __name__ == '__main__':
    if(len(sys.argv) > 2):
        print("Too many arguments were passed, only pass the text to be parsed")
        sys.exit(1)
    elif(len(sys.argv) == 2):
        p = Parser()
        p.build()
        text_to_be_parsed = sys.argv[1]
        p.test_doc(text_to_be_parsed)
    elif(len(sys.argv) == 1):
        p = Parser()
        p.build()
        p.test_str()
    

# p.test_str()  # Uncomment for quick testing
# p.test_doc() # <- uncomment for testing
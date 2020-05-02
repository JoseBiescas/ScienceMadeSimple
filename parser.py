import ply.yacc as yacc
import astMatlab as ast
import math

from lexer import Lexer

IDS = {}
IDList = {}

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
        '''program : expression'''
        p[0] = ast.MAIN([p[1]])

    # Done this way so there is precedence clearly stated
    def p_expression_binop(self, p):
        '''expression : expression '+' expression %prec '+'
            | expression '-' expression %prec '-'
            | expression '*' expression %prec '*'
            | expression '/' expression %prec '/'
            | expression '^' expression %prec '^' '''
        p[0] = ast.BINOP(p[2], p[1], p[3])

    def p_expression_unary(self, p):
        '''expression : '-' expression %prec UMINUS'''
        p[0] = ast.UNARY(p[1], p[2])

    def p_expression_par(self, p):
        '''expression : '(' expression ')' '''
        p[0] = p[2]

    def p_expression_assign(self, p):
        '''expression : identifier '=' expression'''
        IDS[p[1]] = p[3]

    # def p_expression_for_loop(self, p):
    #     '''expression : FOR IDList AT List'''

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
             | empty
             | BOOLEAN
             | identifier
             | sciences
             '''
        p[0] = p[1]

    def p_IDList(self, p):
        '''
        IDList : identifier
               | identifier ',' IDList
        '''
        IDList[p[1]] = 0


    def p_IDENTIFIER(self, p):
        '''
        identifier : ID
        '''
        p[0] = IDS.get(p[1], p[1])

    def p_empty(self, p):
        'empty :'
        pass

    def p_BINOP(self, p):
        '''
        BINOP : '+'
              | '-'
              | '*'
              | '/'
              | '='
              | NOTEQ
              | '<'
              | '>'
              | LTOE
              | GTOE
              | '&'
              | '|'
              '''

        p[0] = p[1]

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
               '''
        p[0] = p[1]

    # EPERCENT PARAMETERS: approximate value, exact value
    # FORMULA = (|aprox - exact|/exact) * 100

    def p_SCIENCES(self, p):
        '''
        sciences : physics
                 | chemistry
                 | EPERCENT '(' NUMBER ',' NUMBER ')'
        '''

        if(p[1] == 'epercent'):
            p[0] = (abs(p[3] - p[5])/p[5]) * 100
        else:
            p[0] = p[1]

    def p_PHYSICS(self, p):
        '''
        physics : POSITION '(' NUMBER ',' NUMBER ',' NUMBER ',' NUMBER ')'
                | INITIAL VELOCITY '(' NUMBER ',' NUMBER ',' NUMBER ')'
                | FINAL VELOCITY '(' NUMBER ',' NUMBER ',' NUMBER ',' BOOLEAN ')'
                | AVERAGE VELOCITY '(' NUMBER ',' NUMBER ',' NUMBER ')'
                | VELOCITY IN XAXIS '(' NUMBER ',' NUMBER ')'
                | VELOCITY IN YAXIS '(' NUMBER ',' NUMBER ')'
                | ACCELERATION '(' NUMBER ',' NUMBER ',' NUMBER ')'
                | POTENTIAL ENERGY '(' NUMBER ',' NUMBER ')'
                | KINETIC ENERGY '(' NUMBER ',' NUMBER ')'
        '''

    # POSITION PARAMETERS: acceleration, time, initial velocity and initial position
    # FORMULA = 0.5 * a * t^2 + v0*t + initial position

        if (p[1] == 'position'):
            p[0] = 0.5 * p[3] * p[5]**2 + p[7]*p[5] + p[9]

    # INITIAL VELOCITY PARAMETERS: final velocity, acceleration, displacement
    # FORMULA: sqrt(vF^2 - 2*a*displacement)

        elif (p[1] == 'initial' and p[2] == 'velocity'):
            p[0] = math.sqrt(p[4]**2 - 2 * p[6] * p[8])

    # FINAL VELOCITY:  initial velocity, acceleration, (displacement or time), boolean
    # FORMULA 1: sqrt(v0^2 + 2*a*displacement), if boolean is true
    # FORMULA 2: v0 + a*t, if boolean is false

        elif (p[1] == 'final' and p[2] == 'velocity'):
            if(p[10] == True):
                p[0] = math.sqrt(p[4]**2 + 2 * p[6] * p[8])
            else:
                p[0] = p[4] + p[6] * p[8]

    # AVERAGE VELOCITY PARAMETERS: initial position, final position, time
    # FORMULA = (xF - x0)/t

        elif (p[1] == 'average' and p[2] == 'velocity'):
            p[0] = (p[4]-p[6])/p[8]

    # VELOCITY IN X PARAMETERS: the overall velocity
    # FORMULA: v*cos(theta)

        elif (p[1] == 'velocity' and p[2] == 'in' and p[3] == 'xaxis'):
            p[0] == p[5] * math.cos(p[7])

    # VELOCITY IN Y PARAMETERS: the overall velocity
    # FORMULA: v*sin(theta)

        elif (p[1] == 'velocity' and p[2] == 'in' and p[3] == 'yaxis'):
            p[0] == p[5] * math.sin(p[7])

    # ACCELERATION PARAMETERS: initial velocity, final velocity, time
    # FORMULA: (vF - v0)/t

        elif (p[1] == 'acceleration'):
            p[0] = (p[3]-p[5])/p[7]

    # POTENTIAL ENERGY PARAMETERS: mass, vertical height
    # FORMULA: m * G * h

        elif (p[1] == 'potential' and p[2] == 'energy'):
            p[0] == p[4] * 9.80665 * p[6]

    # KINETIC ENERGY PARAMETERS: mass, velocity
    # FORMULA: 0.5 * m * v^2

        elif (p[1] == 'kinetic' and p[2] == 'energy'):
            p[0] == 0.5 * p[4] * p[6]

    def p_CHEMISTRY(self, p):
        '''
        chemistry : 
        '''

    def p_error(self, p):
        print("Syntax error in input!")

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        print("Built succesfully")

    def test_doc(self):
        while True:
            try:
                f = open("Test", "r")
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
            self.parser.parse(s, debug=True)
            print("Parse finished.")


p = Parser()
p.build()
p.test_str()  # Uncomment for quick testing
# p.test_doc() <- uncomment for testing

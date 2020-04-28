import ply.yacc as yacc

from lexer import Lexer


class Parser():
    m = Lexer()
    m.build()
    tokens = m.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def p_expression_binop(self, p):
        '''expression : expression BINOP expression'''

    def p_expression_par(self, p):
        '''expression : '(' expression ')' '''

    def p_expression_assign(self, p):
        '''expression : ID '=' expression'''

    # def p_expression_for_loop(self, p):
    #     '''expression : FOR IDList AT List'''

    def p_expression_ques(self, p):
        '''expression : expression ',' expression '?' expression'''

    def p_expression(self, p):
        '''expression : TERM'''

    def p_term(self, p):
        '''
        TERM : NUMBER
             | empty
             | BOOLEAN
             | ID
             | '-' NUMBER %prec UMINUS
             '''

    def p_IDList(self, p):
        '''
        IDList : ID
               | ID ',' IDList
        '''

    # def p_IDENTIFIER(self, p):
    #     '''
    #     identifier : ID
    #     '''

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

    def p_BOOLEAN(self, p):
        '''
        BOOLEAN : TRUE
                | FALSE
                '''

    def p_NUMBER(self, p):
        '''
        NUMBER : FLOAT
               | INT
               '''

    # def p_FLOATN(self,p):
    #     '''
    #     FLOATN : FLOAT
    #     '''

    # def p_INTEGER(self,p):
    #     '''
    #     INTEGER : INT
    #     '''

    # EPERCENT PARAMETERS: approximate value, exact value
    # FORMULA = (|aprox - exact|/exact) * 100

    def p_SCIENCES(self, p):
        '''
        sciences : physics
                 | chemistry
                 | EPERCENT '(' NUMBER ',' NUMBER ')'
        '''

    # PHYSICS:
    # POSITION PARAMETERS: acceleration, time, initial velocity and initial position
    # FORMULA = 0.5 * a * t^2 + v0*t + initial position

    # INITIAL VELOCITY PARAMETERS: final velocity, acceleration, displacement
    # FORMULA: sqrt(vF^2 - 2*a*displacement)

    # FINAL VELOCITY:  initial velocity, acceleration, (displacement or time), boolean
    # FORMULA 1: sqrt(v0^2 + 2*a*displacement), if boolean is true
    # FORMULA 2: v0 + a*t, if boolean is false

    # AVERAGE VELOCITY PARAMETERS: initial position, final position, time
    # FORMULA = (xF - x0)/t

    # VELOCITY IN X PARAMETERS: the overall velocity
    # FORMULA: v*cos(theta)

    # VELOCITY IN Y PARAMETERS: the overall velocity
    # FORMULA: v*sin(theta)

    # ACCELERATION PARAMETERS: initial velocity, final velocity, time
    # FORMULA: (vF - v0)/t

    # POTENTIAL ENERGY PARAMETERS: mass, vertical height
    # FORMULA: m * G * h

    # KINETIC ENERGY PARAMETERS: mass, velocity
    # FORMULA: 0.5 * m * v^2
    # #
    def p_PHYSICS(self, p):
        '''
        physics : POSITION '(' NUMBER ',' NUMBER ',' NUMBER ',' NUMBER ')'
                | INITIAL VELOCITY '(' NUMBER ',' NUMBER ',' NUMBER ')'
                | FINAL VELOCITY '(' NUMBER ',' NUMBER ',' NUMBER ',' BOOLEAN ')'
                | AVERAGE VELOCITY '(' NUMBER ',' NUMBER ',' NUMBER ')'
                | VELOCITY IN XAXIS '(' NUMBER ')'
                | VELOCITY IN YAXIS '(' NUMBER ')'
                | ACCELERATION '(' NUMBER ',' NUMBER ',' NUMBER ')'
                | POTENTIAL ENERGY '(' NUMBER ',' NUMBER ')'
                | KINETIC ENERGY '(' NUMBER ',' NUMBER ')'
        '''

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
p.test_str() #Uncomment for quick testing
# p.test_doc() <- uncomment for testing

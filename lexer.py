import ply.lex as lex
from ply.lex import TOKEN

class Lexer(object):

    keywords = {
        'for' : 'FOR',
        'at' : 'AT',
        'while' : 'WHILE',
        'stop' : 'STOP',
        'next' : 'NEXT',
        'in' : 'IN',
        'show' : 'SHOW',
        'from' : 'FROM',
        'to' : 'TO',
        'func' : 'FUNC',

        #physics
        'position' : 'POSITION', 
        'kineticEnergy' : 'KINETICENERGY', 
        'potentialEnergy' : 'POTENTIALENERGY',  
        'acceleration' : 'ACCELERATION', 
        'impulse' : 'IMPULSE',
        'initialVelocity' : 'INITIALVELOCITY',
        'finalVelocity' : 'FINALVELOCITY',
        'averageVelocity' : 'AVERAGEVELOCITY',
        'velocityX' : 'VELOCITYX',
        'velocityY' : 'VELOCITYY',
        'time' : 'TIME',
        'force' : 'FORCE',
        
        #chemistry
        'broglie': 'BROGLIE', 
        'coulomb': 'COULOMB',
        'heatTransfer' : 'HEATTRANSFER',
        'bfp' : 'BFP',
        'epercent' : 'EPERCENT', 
        'gravity' : 'GRAVITY', 
        'planck' : 'PLANCK', 
        
        #math
        'pi' : 'PI',
        'eulier' : 'EULIER',
        'integralApproximation' : 'INTEGRALAPPROXIMATION',
        'integral' : 'INTEGRAL',
        'derivative' : 'DERIVATIVE',
        'dotProduct' : 'DOTPRODUCT',
        'crossProduct' : 'CROSSPRODUCT',
        'summation' :  'SUMMATION'
    }
    literals = [
        '+', '-', '/', '*', '^', '(', ')', '[',
     ']', '{', '}', '|', '&', '?', '=', '<', '>', ',', ':'
     ]

    tokens = list(keywords.values()) + [

        #Identifier
        'ID',

        #Operators (Can't be decalred in literals)
        'LTOE', 'GTOE', 'NOTEQ', 'EQEQ',

        #Digits
        'INT', 'FLOAT',

        #Booleans
        'TRUE', 'FALSE',

        #String
        'STRING'
    ]

    states = (
        ('comment', 'exclusive'),
    )

    #RULES
    t_LTOE = r'<='
    t_GTOE = r'>='
    t_NOTEQ = r'!='
    t_EQEQ = r'=='
    t_ignore = ' \t'

    def t_singleComment(self,t):
        r'\#+.*'
        pass
    
    def t_startComment(self,t):
        r'/\#'
        t.lexer.begin('comment')
    
    def t_comment_end(self,t):
        r'\#/'
        t.lexer.begin('INITIAL')
    
    t_comment_ignore= " \t\n"

    def t_comment_error(self, t):
     t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += 1
        pass

    def t_ID(self, t):
        r'[a-zA-Z][a-zA-Z0-9_]*'
        t.type = self.keywords.get(t.value, t.type)
        return t

    def t_TRUE(self,t):
        r'true'
        t.value = True
        return t

    def t_FALSE(self, t):
        r'false'
        t.value = False
        return t
    
    def t_FLOAT(self, t):
        r'([0-9]*)?[.][0-9]+'
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        t.value = str(t.value[1:len(t.value) - 1])
        return t

    def t_error(self, t):
        print("Illegal character %s" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self,data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok: 
                break
            print(tok)

m = Lexer()
m.build()

#m.test()#Uncomment to test lexer, must pass in a string
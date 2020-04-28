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

        'position' : 'POSITION', 
        'kinetic' : 'KINETIC', 
        'potential' : 'POTENTIAL', 
        'energy' : 'ENERGY', 
        'velocity' : 'VELOCITY', 
        'acceleration' : 'ACCELERATION', 
        'impulse' : 'IMPULSE', 
        'epercent' : 'EPERCENT', 
        'gravity' : 'GRAVITY', 
        'planck' : 'PLANCK', 
        'pi' : 'PI',
        'initial' : 'INITIAL',
        'final' : 'FINAL',
        'average' : 'AVERAGE',
        'time' : 'TIME',
        'force' : 'FORCE',
        'xaxis' : 'XAXIS',
        'yaxis' : 'YAXIS'
    }
    literals = [
        '+', '-', '/', '*', '^', '(', ')', '[',
     ']', '{', '}', '|', '&', '?', '=', '<', '>', ','
     ]

    tokens = list(keywords.values()) + [

        #Identifier
        'ID',

        #Operators (Can't be decalred in literals)
        'LTOE', 'GTOE', 'NOTEQ',

        #Digits
        'INT', 'FLOAT',

        #Booleans
        'TRUE', 'FALSE',
    ]

    #RULES
    t_LTOE = r'<='
    t_GTOE = r'>='
    t_NOTEQ = r'!='
    t_ignore = ' \t'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += 1
        pass

    def t_ID(self, t):
        r'[a-zA-Z][a-zA-Z0-9]*'
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
#m.test() #Uncomment to test lexer, must pass in a string
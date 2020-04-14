import ply.yacc as yacc

from lexer import Lexer

class Parser():
    m = Lexer()
    m.build()
    tokens = m.tokens


    def p_TERM(self,p):
        '''
        TERM : NUMBER
             | '+' NUMBER
             | '-' NUMBER
             | IDENTIFIER
             | empty
             | BOOLEAN
             '''

    def p_IDList(self,p):
        '''
        IDList : IDENTIFIER
               | IDENTIFIER ',' IDList
        '''

    def p_empty(self,p):
        'empty :'
        pass
    
    def p_BINOP(self,p):
        '''
        BINOP : '+'
              | '-'
              |'*'
              |'/'
              |'='
              |'!''='
              |'<'
              |'>'
              |'<''='
              |'>''='
              |'&'
              |'|'
              '''

    def p_BOOLEAN(self,p):
        '''
        BOOLEAN : TRUE
                | FALSE
                '''
    
    def p_IDENTIFIER(self,p):
        '''
        IDENTIFIER : ID
        '''

    def p_NUMBER(self, p):
        '''
        NUMBER : INTEGER
               | FLOATN
               '''

    def p_FLOATN(self,p):
        '''
        FLOATN : FLOAT
        '''

    def p_INTEGER(self,p):
        '''
        INTEGER : INT
        '''
    
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self,**kwargs)
        print("Built succesfully")
    
    def test(self):
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
p = Parser()
p.build()
#p.test() <- uncomment for testing
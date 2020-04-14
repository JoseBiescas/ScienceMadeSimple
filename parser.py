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
    
    def p_error(self, p):
        print("Syntax error in input!")
    
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self,**kwargs)
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
#p.test_str() Uncomment for quick testing 
#p.test_doc() <- uncomment for testing
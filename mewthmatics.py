import ply.lex as lex
import ply.yacc as yacc

class Mewlex():
    tokens = (
        'DIVIDE',
        'MINUS',
        'POW',
        'TIMES',
        'DOT',
        'PLUS',
        'NUMBER'
    )

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.result_lex = []
    
    def t_DIVIDE(self, t):
        r'\/'
        return t

    def t_MINUS(self, t):
        r'\-'
        return t
    def t_POW(self, t):
        r'\^'
        return t

    def t_TIMES(self, t):
        r'\*'
        return t
    def t_DOT(self, t):
        r'\.'
        return t
    def t_PLUS(self, t):
        r'\+'
        return t

    def t_NUMBER(self, t):
        r'\d+\.\d+|\d+'
        if t.value.find('.'):
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t): 
        print('Caracter no valido', t.value[0])
        t.lexer.skip(1)

    t_ignore = '\r\t'
    
    def analyze(self, data):
        self.lexer.input(data)

        while True:
            tok = self.lexer.token()
            if not tok:
                break
            self.result_lex.append((tok.value, tok.type))
            

class Mewyacc():
    def __init__(self):
        self.mewlex = Mewlex
        self.tokens = Mewlex.tokens
        self.parser = yacc.yacc(module=self)
        self.__result = 0

    ### grammar
    def p_expr(self, p):
        '''expr : expr PLUS expr
                | expr MINUS expr
                | expr TIMES expr
                | expr DIVIDE expr
                | expr POW expr 
                | NUMBER'''
        try:
            if p[2] == '+':
                p[0] = p[1] + p[3]
                self.__result = p[0]

            elif p[2] == '-':
                p[0] = p[1] - p[3]
                self.__result = p[0]

            elif p[2] == '*':
                p[0] = p[1] * p[3]
                self.__result = p[0]

            elif p[2] == '/':
                p[0] = p[1] / p[3]
                self.__result = p[0]
            elif p[2] == '^':
                p[0] = p[1] ** p[3]
                self.__result = p[0]
        except:
            if type(p[1]) == int:
                p[0] = p[1]
                self.__result = p[0]
            if type(p[1]) == float:
                p[0] = p[1]
                self.__result = p[0]

    def p_error(self, p):
        if p:
            self.__result = f"Syntax error at token {p.value}"

        else:
            self.__result = "Syntax error at EOF" 


    def analyze(self, data):
        self.parser.parse(data, lexer=self.mewlex().lexer)
        return self.__result



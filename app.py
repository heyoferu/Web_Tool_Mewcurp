from flask import Flask, render_template, request
import ply.lex as lex
import ply.yacc as yacc
import random
import string

class Mewlex():
    tokens = (
        'CHAR',
        'NUMBER'
    )

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.result_lex = []
    
    def t_CHAR(self, t):
        r'[A-Z]'
        return t

    def t_NUMBER(self, t):
        r'\d'
        return t

    def t_KEY(self, t):
        r'\b\d{2}\b'
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
        pass

    def p_error(self, p):
        if p:
            self.__result = f"Syntax error at token {p.value}"

        else:
            self.__result = "Syntax error at EOF" 


    def analyze(self, data):
        self.parser.parse(data, lexer=self.mewlex().lexer)
        return self.__result


class Mewcurp:
    def __init__(self):
        self.generated_curp = ""
        self.__vowels = 'AEIOU'


    def gen(self, name, lastname_1, lastname_2, year, month, day, sex, state):
        
        temp = lastname_1[0] + self.get_vowel(lastname_1) + lastname_2[0] + name[0] + year + month + day + sex + state + self.get_next_consonant(lastname_1) + self.get_next_consonant(lastname_2) + self.get_next_consonant(name) + self.hkey()

        return temp

    def get_vowel(self, data):
        for char in data:
            if char in self.__vowels:
                return char

    def get_next_consonant(self, data):
        for char in data[1:]:
            if char not in self.__vowels:
                return char
        
    def hkey(self):
        return ''.join(random.choices(string.ascii_uppercase + '0123456789', k=2))
        


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name').upper()
        lname_1 = request.form.get('lastname_1').upper()
        lname_2 = request.form.get('lastname_2').upper()
        year = request.form.get('year')[2:]
        month = request.form.get('month')
        day = request.form.get('day')
        sex = request.form.get('sex')
        state = request.form.get('state')
        
                
    
        curp = Mewcurp()
        result = curp.gen(name, lname_1, lname_2, year, month, day, sex, state)
        

        return render_template('curp.html', curp = result, name = name, lastname_1 = lname_1, lastname_2 = lname_2,  year = year, month = month, day = day, sex = sex, state = state)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

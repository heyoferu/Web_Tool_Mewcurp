from flask import Flask, render_template, request
import ply.lex as lex
import ply.yacc as yacc
import random
import string
from cities import cities
from words import restricted_words

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
        self.__result = None

    ### CURP validate
    def p_curp(self, p):
        '''curp : prefix date CHAR CHAR CHAR CHAR CHAR CHAR key'''

    def p_prefix(self, p):
        '''prefix : CHAR CHAR CHAR CHAR'''
        p[0] = p[1] + p[2] + p[3] + p[4]
        if p[0] in restricted_words:
            p[0] = restricted_words[p[0]]
        else:
            pass
        
    def p_date(self, p):
        '''date : NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER'''
        if p[3] + p[4] == '02' and int(p[5] + p[6]) > 2:
            self.__result ="Febrero tiene 28 dias"
           
            
        if p[3] + p[4] not in ['01','03','05','07','08','10','12'] and int(p[5] + p[6]) > 30:
            self.__result = f"El mes seleccionado tiene 30 días"
    
    def p_key(self, p):
        '''key : CHAR NUMBER
               | NUMBER CHAR
               | CHAR CHAR
               | NUMBER NUMBER'''
    
    def p_error(self, p):
        if p:
            self.__result = f"Syntax error at token {p.value} at line {p.lineno} pos {p.lexpos}"

        else:
            self.__result = "Syntax error at EOF" 


    def analyze(self, data):
        self.parser.parse(data, lexer=self.mewlex().lexer)
        return self.__result
        

class Mewcurp:
    def __init__(self):
        self.generated_curp = ""
        self.__vowels = 'AEIOU'


    def gen(self, name, lastname_1, lastname_2, year, month, day, gen, state):
        
        temp = lastname_1[0] + self.get_vowel(lastname_1) + lastname_2[0] + name[0] + year + month + day + gen + state + self.get_next_consonant(lastname_1) + self.get_next_consonant(lastname_2) + self.get_next_consonant(name) + self.hkey()

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
        gen = request.form.get('gen')
        state = request.form.get('state')
        
        print(request.form)
                
        curp = Mewcurp()
        curp_result = curp.gen(name, lname_1, lname_2, year, month, day, gen, state)


        validate_curp = Mewyacc()
        error = validate_curp.analyze(curp_result)
        if error:
            return render_template('curp.html', curp = error)

        return render_template('curp.html', curp = curp_result, name = name, lastname_1 = lname_1, lastname_2 = lname_2,  year = year, month = month, day = day, gen = 'Masculino' if gen == 'H' else 'Femenino', state = cities[state])
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

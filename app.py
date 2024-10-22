from flask import Flask, render_template, request
from mewthmatics import Mewlex, Mewyacc

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        button = request.form.get('button')
        if button == 'result':
            expr = request.form.get('cal_display')
            mew = Mewyacc()
            catlex = Mewlex()
            catlex.analyze(expr)
            result = mew.analyze(expr)
            tokens = catlex.result_lex
            return render_template('index.html', input=expr, tokens=tokens, result=result)

        elif button == 'clear':
            return render_template('index.html')
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, url_for, redirect, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab8 import lab8
from lab7 import lab7
from lab9 import lab9
from rgz import rgz

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz)

app.config['DB_TYPE'] = 'postgres'
app.secret_key = ')))'
@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename = "404.jpg")
    style = url_for("static", filename = "lab1.css")
    return '''
<!doctype html>
<html>
<head>
    <link rel = "stylesheet" href="''' + style +'''"
</head>
    <body>
        <img src="''' + path + '''" class="full-screen-image">
    </body>
</html>
''', 404

@app.route('/')
@app.route('/index')
def index():
    style = url_for("static", filename = "lab1.css")
    return '''<!doctype html>
        <html>
        <head>
            <link rel = "stylesheet" href="''' + style +'''"
            <title>НГТУ, ФБ, Лабораторные работы</title>
        </head>
        <header>
                НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <body>
                <a href='/lab1'>Первая лабораторная</a>
                <a href='/lab2'>Вторая лабораторная</a>
                <a href='/lab3'>Третья лабораторная</a>
                <a href='/lab4'>Четвертая лабораторная</a>
                <a href='/lab5'>Пятая лабораторная</a>
                <a href='/lab6'>Шестая лабораторная</a>
                <a href='/lab7'>Седьмая лабораторная</a>
                <a href='/lab8'>Восьмая лабораторная</a>
                <a href='/lab9'>Девятая лабораторная</a> 
                <a href='/rgz'>rgz</a> 
        </body>
        <footer>Токарский Илья Андреевич, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200


@app.route('/error/400')
def error_400():
    return 'Bad Request', 400

@app.route('/error/401')
def error_401():
    return 'Unauthorized', 401

@app.route('/error/402')
def error_402():
    return 'Payment Required', 402

@app.route('/error/403')
def error_403():
    return 'Forbidden', 403

@app.route('/error/405')
def error_405():
    return 'Method Not Allowed', 405

@app.route('/error/418')
def error_418():
    return "I'm a teapot", 418

@app.route('/trigger_error')
def trigger_error():
    # Вызываем ошибку деления на ноль
    return 1 / 0

@app.errorhandler(500)
def internal_error(error):
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка сервера</title>
    </head>
    <body>
        <h1>Произошла ошибка на сервере</h1>
        <p>Пожалуйста, попробуйте позже.</p>
    </body>
</html>
''', 500

@app.route('/model')
def heavy_metal():
    path = url_for("static", filename = "Bella.jpg")
    style = url_for("static", filename = "lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel = "stylesheet" href="''' + style +'''"
        <title>BELLA HADID</title>
        <style>
            body {
                background-color: black;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>Bella</h1>
        <p>
           маделирую шмаделирую чиста э уа афап
        </p>
        <img src="''' + path + '''" alt="Bella">
    </body>
</html>
''', 200, {
    'Content-Language': 'ru',
    'X-Custom-Header-1': 'bella',
    'X-Custom-Header-2': 'bella'
}


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, url_for, redirect, render_template

app = Flask(__name__)

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
           </body>
           <footer>Токарский Илья Андреевич, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200

@app.route('/lab1')
def lab1():
    style = url_for("static", filename = "lab1.css")
    return '''<!doctype html>
        <html>
        <head>
            <link rel = "stylesheet" href="''' + style +'''"
            <title>Лабораторная 1</title>
        </head>
        <body>
                <p>
                    Flask — фреймворк для создания веб-приложений на языке
                    программирования Python, использующий набор инструментов
                    Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                    называемых микрофреймворков — минималистичных каркасов
                    веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
                </p>
                <a href="/">Главная страница</a>
                <h2>Список роутов</h2>
                <ul>
                    <li><a href="/">Главная страница</a></li>
                    <li><a href="/index">Главная страница (index)</a></li>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab1/web">Web</a></li>
                    <li><a href="/lab1/author">Автор</a></li>
                    <li><a href="/lab1/oak">Дуб</a></li>
                    <li><a href="/lab1/counter">Счетчик</a></li>
                    <li><a href="/lab1/cancel_counter">Сброс счетчика</a></li>
                    <li><a href="/lab1/info">Информация</a></li>
                    <li><a href="/lab1/created">Создано успешно</a></li>
                    <li><a href="/error/400">Ошибка 400</a></li>
                    <li><a href="/error/401">Ошибка 401</a></li>
                    <li><a href="/error/402">Ошибка 402</a></li>
                    <li><a href="/error/403">Ошибка 403</a></li>
                    <li><a href="/error/405">Ошибка 405</a></li>
                    <li><a href="/error/418">Ошибка 418</a></li>
                    <li><a href="/trigger_error">Триггер ошибки</a></li>
                    <li><a href="/model">Белла Хадид</a></li>
                </ul>
        </body>
        <footer>Токарский Илья Андреевич, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200

@app.route('/lab1/web')
def start():
    return '''<!doctype html>
        <html>
           <body>
                <h1>web-сервер на flask</h1>
                <a href='author'>author</a>  
                <a href='/lab1/oak'>дуб</a> 
           </body>
        </html>''', 200, {
            'X-Server,': 'sample',
            'Content-type': 'text/plain; charset=utf-8'
                          }

@app.route('/lab1/author')
def author():
    name = 'Токарский Илья Андреевич'
    group = 'ФБИ-22'
    faculty = 'ФБ'

    return '''<!doctype html>
        <html>
           <body>
                <p>Студент: ''' + name + '''</p>
                <p>Группа: ''' + group + '''</p>
                <p>Факультет: ''' + faculty + '''</p>
                <a href='web'>web</a>
                <a href='/lab1/oak'>дуб</a>
           </body>
        </html>'''

@app.route('/lab1/oak')
def oak():
    path = url_for("static", filename = "oak.jpg")
    style = url_for("static", filename = "lab1.css")
    return '''
<!doctype html>
<html>
    <link rel = "stylesheet" href="''' + style +'''"
    <body>
        <h1>дубик хихи)</h1>
        <img src="''' + path + '''" class="oak-image">
    </body>
</html>
'''

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    reset_link = url_for('cancel_counter')
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <br>
        <a href="''' + reset_link + '''">Очистить счётчик</a>
    </body>
</html>
'''

@app.route('/lab1/cancel_counter')
def cancel_counter():
    global count
    count = 0
    return redirect(url_for('counter'))

@app.route('/lab1/info')
def info():
    return redirect('/lab1/author')

@app.route('/lab1/created')
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

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

@app.route('/lab2/a')
def a():
    return 'ok'

@app.route('/lab2/a/')
def aa():
    return 'ok s /'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flower/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "Такого цветка нет", 404
    else:
        flower_name = flower_list[flower_id]
        return f'''
        <html>
        <head>
            <title>Цветок</title>
        </head>
        <body>
            <h1>Цветок: {flower_name}</h1>
            <a href="/lab2/flowers">Посмотреть все цветы</a>
        </body>
        </html>
        '''

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    if name in flower_list:
        return f'''
        <!doctype html>
        <html>
            <body>
            <h1>Такой цветок уже есть, попробуй другой</h1>
            <p>Список цветков: {flower_list} </p>
            </body>
        </html>'''
    else: 
        flower_list.append(name)
        return f'''
        <!doctype html>
        <html>
            <body>
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка: {name} </p>
            <p>Список цветков: {flower_list} </p>
            </body>
        </html>'''        

@app.route('/lab2/example')
def example():
    name = 'Токарский Илюха.'
    group = 'ФБИ-22'
    year = 2024
    course = 3 
    lab_num = 2
    fruits = [
        {'name': 'яблоки', 'price' : 100},
        {'name': 'груши', 'price' : 120},
        {'name': 'апельсины', 'price' : 80},
        {'name': 'мандарины', 'price' : 95},
        {'name': 'манго', 'price' : 321}
        ]
    
    return render_template('example.html', name=name, group=group, year=year, course=course, lab_num=lab_num, fruits=fruits)

@app.route('/lab2/')
def lab2_main():
    style = url_for("static", filename = "lab1.css")
    links = [
        {"url": "/lab2/example", "text": "example"},
        {"url": "/lab2/a", "text": "/lab2/a"},
        {"url": "/lab2/a/", "text": "/lab2/a/"},
        {"url": "/lab2/flower/1", "text": "Кол-во цветов"},
        {"url": "/lab2/filters", "text": "Фильтры"},
        {"url": "/lab2/add_flower/rose", "text": "Добавить цветок"},
        {"url": "/lab2/add_flower/", "text": "Цветочек без названия"},
        {"url": "/lab2/flowers", "text": "Список цветов и кол-во"},
        {"url": "/lab2/clear_flowers", "text": "Очистка списка цветов"},
        {"url": "/lab2/calc/14/28", "text": "Калькуляторчик"},
        {"url": "/lab2/calc/1", "text": "Перенаправление"},
    ]

    return render_template('lab2.html', links=links, style=style)

@app.route('/lab2/filters')
def filters():
    phrase = 'как <b>же</b> <u>круто</u> <i>быть</i> рокстар..'
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/add_flower/')
def flower_f():
    return 'Вы не задали имя цветка', 400

@app.route('/lab2/flowers')
def all_flowers():
    return f'''
    <p>Список цветков: {', '.join(flower_list)}</p>
    <p>Количество цветов: {len(flower_list)}</p>
    '''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list = []
    return '''
    <html>
    <head>
        <title>Список цветов очищен</title>
    </head>
    <body>
        <h1>Список цветов очищен</h1>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
    </body>
    </html>
    '''

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    result_1 = a + b
    result_2 = a - b
    result_3 = a * b
    result_4 = a / b
    result_5 = a ** b
    return '''
    <html>
    <head>
        <title>Расчёт с параметрами</title>
    </head>
    <body>
        <h1>Расчёт с параметрами</h1>
        <p>{a} + {b} = {result_1}</p>
        <p>{a} - {b} = {result_2}</p>
        <p>{a} * {b} = {result_3}</p>
        <p>{a} / {b} = {result_4}</p>
        <p>{a} ^ {b} = {result_5}</p>
    </body>
    </html>
    '''.format(a=a, b=b, result_2=result_2, result_1=result_1, result_3=result_3, result_4=result_4, result_5=result_5)

@app.route('/lab2/calc/<int:a>')
def redirect_to_default(a):
    return redirect(f'/lab2/calc/{a}/1')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/lab2/a1/')
def a1():
    return 'со слешем'

@app.route('/lab2/a2')
def a2():
    return 'без слеша'
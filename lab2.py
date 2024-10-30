from flask import Blueprint, url_for, redirect, render_template
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'ok'


@lab2.route('/lab2/a/')
def aa():
    return 'ok s /'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']


@lab2.route('/lab2/flower/<int:flower_id>')
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


@lab2.route('/lab2/add_flower/<name>')
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
        flower_list.lab2end(name)
        return f'''
        <!doctype html>
        <html>
            <body>
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка: {name} </p>
            <p>Список цветков: {flower_list} </p>
            </body>
        </html>'''        


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/')
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


@lab2.route('/lab2/filters')
def filters():
    phrase = 'как <b>же</b> <u>круто</u> <i>быть</i> рокстар..'
    return render_template('filter.html', phrase=phrase)


@lab2.route('/lab2/add_flower/')
def flower_f():
    return 'Вы не задали имя цветка', 400


@lab2.route('/lab2/flowers')
def all_flowers():
    return f'''
    <p>Список цветков: {', '.join(flower_list)}</p>
    <p>Количество цветов: {len(flower_list)}</p>
    '''


@lab2.route('/lab2/clear_flowers')
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


@lab2.route('/lab2/calc/<int:a>/<int:b>')
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

@lab2.route('/lab2/calc/<int:a>')
def redirect_to_default(a):
    return redirect(f'/lab2/calc/{a}/1')

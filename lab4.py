from flask import Blueprint, url_for, redirect, render_template, request, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab4_main():
    name_color = request.cookies.get('name_color')
    name = request.cookies.get('name')
    age = 18
    links = [
        {"url": "/lab4/div-form", "text": "Деление"},
        {"url": "/lab4/sum-form", "text": "Cумма"},
        {"url": "/lab4/sub-form", "text": "Вычитание"},
        {"url": "/lab4/mul-form", "text": "Умножение"},
        {"url": "/lab4/pow-form", "text": "Cтепень"},
        {"url": "/lab4/tree", "text": "Дерево"},
        {"url": "/lab4/login", "text": "Логин"},
        {"url": "/lab4/cold", "text": "Холодос"},
        {"url": "/lab4/zerno-form", "text": "Зерно"},
    ]
    return render_template('/lab4/lab4.html', links=links, name=name, name_color=name_color, age=age)


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('/lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('/lab4/div.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('/lab4/div.html', error='Анлаки нолик')
    result = x1 / x2
    return render_template('/lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('/lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('/lab4/sum.html', x1=x1, x2=x2, result=result)




@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('/lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('/lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('/lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('/lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    result = x1 - x2
    return render_template('/lab4/sub.html', x1=x1, x2=x2, result=result)




@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('/lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('/lab4/pow.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('/lab4/pow.html', error='Нельзя возводить 0 в степень 0!')
    result = x1 ** x2
    return render_template('/lab4/pow.html', x1=x1, x2=x2, result=result)



tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')
    
    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        tree_count += 1
    else:
        return "Операция не выбрана", 400
        
    return redirect(url_for('lab4.tree'))


users = [
    {'login': 'Alex', 'password': '123', 'name': 'Александр', 'gender': 'male'},
    {'login': 'Bob', 'password': '555', 'name': 'Боб', 'gender': 'male'},
    {'login': '9mice', 'password': '777', 'name': 'Мышь', 'gender': 'female'},
    {'login': 'kaiangel', 'password': '888', 'name': 'Катя', 'gender': 'female'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        authorized = 'login' in session
        login = session.get('login', '')
        return render_template('/lab4/login.html', authorized=authorized, login=login)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'не введён логин'
        return render_template('/lab4/login.html', error=error, authorized=False, login=login)

    if not password:
        error = 'не введён пароль'
        return render_template('/lab4/login.html', error=error, authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/qq')
    
    error = 'неверные логин и/или пароль'
    return render_template('/lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/qq')
def qq():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    name = session['name']
    return render_template('/lab4/qq.html', name=name)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/cold', methods=['GET', 'POST'])
def cold():
    message = None
    snowflakes = 0

    if request.method == 'POST':
        temperature = request.form.get('temperature')

        if not temperature:
            message = "ошибка: не задана температура"
        else:
            temperature = float(temperature)

            if temperature < -12:
                message = "не удалось установить температуру — слишком низкое значение"
            elif temperature > -1:
                message = "не удалось установить температуру — слишком высокое значение"
            elif -12 <= temperature <= -9:
                message = f"Установлена температура: {temperature}°С"
                snowflakes = 3
            elif -8 <= temperature <= -5:
                message = f"Установлена температура: {temperature}°С"
                snowflakes = 2
            elif -4 <= temperature <= -1:
                message = f"Установлена температура: {temperature}°С"
                snowflakes = 1

    return render_template('lab4/cold.html', message=message, snowflakes=snowflakes)




@lab4.route('/lab4/zerno-form')
def zerno_form():
    return render_template('/lab4/zerno-form.html')

@lab4.route('/lab4/zerno', methods=['POST'])
def zerno():
    zerno_type = request.form.get('zerno')  
    weight = request.form.get('weight')

    if weight == '':
        return render_template('/lab4/zerno.html', error='Укажите вес')

    weight = int(weight)

    if weight <= 0:
        return render_template('/lab4/zerno.html', error='Вес должен быть больше > 0 ')

    if weight > 500:
        return render_template('/lab4/zerno.html', error='Такого объёма у нас нет')

    if zerno_type == "Ячмень":
        price_per_ton = 12345
    elif zerno_type == "Овёс":
        price_per_ton = 8522
    elif zerno_type == "Пшеница":
        price_per_ton = 8722
    else:
        price_per_ton = 14111

    total_cost = price_per_ton * weight

    discount = 0
    if weight > 50:
        discount = total_cost * 0.1
        total_cost -= discount

    return render_template('/lab4/zerno.html', zerno=zerno_type, weight=weight, total_cost=total_cost, discount=discount)
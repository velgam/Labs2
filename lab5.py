from flask import Blueprint, url_for, redirect, render_template, request, session
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab_main():
    name_color = request.cookies.get('name_color')
    name = request.cookies.get('name')
    age = 18
    links = [
        {"url": "/lab5/login", "text": "вход"},
        {"url": "/lab5/register", "text": "регистраиця"},
        {"url": "/lab5/list", "text": "список статей"},
        {"url": "/lab5/create", "text": "создать статью"},
    ]
    return render_template('/lab5/lab5.html', links=links, name=name, name_color=name_color, age=age)
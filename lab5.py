from flask import Blueprint, url_for, redirect, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

lab5 = Blueprint('lab5', __name__)

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='velgam_base',
        user='velgam_base',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля!')

    conn, cur = db_connect()
    cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error='Заполните поля')

    conn, cur = db_connect()
    cur.execute("SELECT login, password FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    conn, cur = db_connect()
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    user_id = cur.fetchone()["id"]

    cur.execute("INSERT INTO articles(user_id, title, article_text) VALUES (%s, %s, %s);", (user_id, title, article_text))
    db_close(conn, cur)
    return redirect('/lab5/')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    conn, cur = db_connect()
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    user_id = cur.fetchone()["id"]

    cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC;", (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)

    if not articles:
        return render_template('/lab5/articles.html', articles=articles, no_articles=True)

    return render_template('/lab5/articles.html', articles=articles)

@lab5.route('/lab5/logout')
def logout():
    session.clear()
    return redirect('/lab5/login')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена", 404

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/users')
def users():
    conn, cur = db_connect()
    cur.execute("SELECT login FROM users;")
    users = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/public_articles')
def public_articles():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM articles WHERE is_public=true;")
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)

@lab5.route('/lab5/toggle_public/<int:article_id>', methods=['POST'])
def toggle_public(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    cur.execute("SELECT is_public FROM articles WHERE id=%s;", (article_id,))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена", 404

    new_is_public = not article['is_public']
    cur.execute("UPDATE articles SET is_public=%s WHERE id=%s;", (new_is_public, article_id))
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    article = cur.fetchone()

    # Удаляем статью
    cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    db_close(conn, cur)

    return redirect('/lab5/list')
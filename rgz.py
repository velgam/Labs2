from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import logging
rgz = Blueprint('rgz', __name__)
rgz.secret_key = 'your_secret_key'

from werkzeug.security import generate_password_hash

password = '123'  
password_hash = generate_password_hash(password)
print(password_hash)

#  -- Таблица пользователей
#  CREATE TABLE users (
#      id SERIAL PRIMARY KEY,
#      username VARCHAR(50) UNIQUE NOT NULL,
#      password_hash VARCHAR(255) NOT NULL,
#      is_admin BOOLEAN DEFAULT FALSE
#  );

#  -- Таблица инициатив
#  CREATE TABLE initiatives (
#      id SERIAL PRIMARY KEY,
#      title VARCHAR(255) NOT NULL,
#      content TEXT NOT NULL,
#      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#      user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
#      votes INT DEFAULT 0
# );

# CREATE TABLE votes (
#      user_id INT NOT NULL,
#      initiative_id INT NOT NULL,
#      vote_value INT CHECK (vote_value IN (-1, 1)),  -- Голос: -1 (Против) или +1 (За)
#     PRIMARY KEY (user_id, initiative_id),
#     FOREIGN KEY (user_id) REFERENCES users(id),
#     FOREIGN KEY (initiative_id) REFERENCES initiatives(id)
# );




# DO $$
# DECLARE
#     i INT;
#     random_title VARCHAR(255);
#     random_content TEXT;
#     random_user_id INT;
#     min_user_id INT;
#     max_user_id INT;
# BEGIN
#     -- Определяем минимальный и максимальный user_id из таблицы users
#     SELECT MIN(id), MAX(id) INTO min_user_id, max_user_id FROM users;

#     -- Генерация 200 инициатив
#     FOR i IN 1..200 LOOP
#         -- Генерация случайного заголовка
#         random_title := 'Инициатива ' || i || ': ' || 
#             CASE (random() * 5)::INT
#                 WHEN 0 THEN 'Улучшение инфраструктуры'
#                 WHEN 1 THEN 'Экологические меры'
#                 WHEN 2 THEN 'Образовательные программы'
#                 WHEN 3 THEN 'Социальная поддержка'
#                 WHEN 4 THEN 'Культурные мероприятия'
#                 WHEN 5 THEN 'Технологические инновации'
#             END;

#         -- Генерация случайного содержимого
#         random_content := 'Описание инициативы ' || i || ': ' ||
#             CASE (random() * 5)::INT
#                 WHEN 0 THEN 'Предлагается улучшить дорожное покрытие в центральных районах города.'
#                 WHEN 1 THEN 'Необходимо внедрить раздельный сбор мусора во всех районах.'
#                 WHEN 2 THEN 'Планируется открытие новых курсов для школьников по программированию.'
#                 WHEN 3 THEN 'Организация бесплатных обедов для малоимущих семей.'
#                 WHEN 4 THEN 'Проведение ежегодного фестиваля искусств.'
#                 WHEN 5 THEN 'Разработка мобильного приложения для управления городскими услугами.'
#             END;

#         -- Генерация случайного user_id в пределах существующих id
#         random_user_id := (random() * (max_user_id - min_user_id) + min_user_id)::INT;

#         -- Вставка инициативы в таблицу
#         INSERT INTO initiatives (title, content, user_id, votes)
#         VALUES (random_title, random_content, random_user_id, (random() * 100)::INT);
#     END LOOP;
# END $$;



# UPDATE users
# SET password_hash = 'scrypt:32768:8:1$QLLDgtCGl8BcqiXu$1e7c31ca31775460de52e626e40c04cc45b1a0420601756f5da9c68d48b6f5fe5aa908af13779a3cd6d5d59c3c2ac4decc49a7e4f9dd6336a06d34f89017b82e'
# WHERE username = 'admin';


# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="tok",
    user="tok",
    password="123",
    host="localhost",
    port="5432"
)

@rgz.route('/rgz')
def indexx():
    offset = request.args.get('offset', default=0, type=int)  # Получаем параметр offset из запроса
    limit = 20  # Количество инициатив на странице

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Получаем все инициативы
            cursor.execute(
                "SELECT * FROM initiatives ORDER BY created_at DESC LIMIT %s OFFSET %s;",
                (limit, offset)
            )
            initiatives = cursor.fetchall()

            # Получаем инициативы текущего пользователя, если он авторизован
            my_initiatives = []
            if 'user_id' in session:
                cursor.execute(
                    "SELECT * FROM initiatives WHERE user_id = %s ORDER BY created_at DESC;",
                    (session['user_id'],)
                )
                my_initiatives = cursor.fetchall()

            conn.commit()
    except Exception as e:
        conn.rollback()
        flash(f'Error: {e}', 'danger')
        initiatives = []
        my_initiatives = []

    return render_template('rgz/rgz.html', initiatives=initiatives, my_initiatives=my_initiatives, offset=offset, limit=limit)

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def registetr():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        try:
            with conn.cursor() as cursor:
                # Пытаемся добавить нового пользователя
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (%s, %s);",
                    (username, password_hash)
                )
                conn.commit()  # Сохраняем изменения
                flash('Регистрация прошла успешно', 'success')
                return redirect('/rgz/login')
        except psycopg2.IntegrityError:
            # Если имя пользователя уже существует
            conn.rollback()  # Откатываем транзакцию
            flash('Имя пользователя уже занято', 'danger')
        except Exception as e:
            # Обработка других ошибок
            conn.rollback()  # Откатываем транзакцию
            flash(f'Ошибка при регистрации: {e}', 'danger')
    return render_template('rgz/register.html')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def loginn():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s;", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['is_admin'] = user['is_admin']
                flash('Login successful', 'success')
                return redirect('/rgz')
            flash('Invalid username or password', 'danger')
    return render_template('rgz/login.html')

@rgz.route('/rgz/logout')
def logoutt():
    session.clear()
    return redirect('/rgz')

@rgz.route('/rgz/create', methods=['GET', 'POST'])
def create_initiativee():
    if 'user_id' not in session:
        flash('Please log in to create an initiative', 'danger')
        return redirect(url_for('rgz.loginn'))  # Исправлено: перенаправление на правильный маршрут

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Title and content are required', 'danger')
            return redirect(url_for('rgz.create_initiativee'))

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO initiatives (title, content, user_id) VALUES (%s, %s, %s);",
                    (title, content, session['user_id'])
                )
                conn.commit()  # Фиксируем транзакцию
                flash('Initiative created successfully', 'success')
                return redirect(url_for('rgz.indexx'))  # Перенаправление на главную страницу
        except Exception as e:
            conn.rollback()  # Откатываем транзакцию в случае ошибки
            flash(f'Error creating initiative: {e}', 'danger')
            return redirect(url_for('rgz.create_initiativee'))

    return render_template('rgz/create.html')



@rgz.route('/rgz/vote/up/<int:id>', methods=['POST'])
def vote_up(id):
    if 'user_id' not in session:
        return redirect('/rgz/login')
    
    try:
        with conn.cursor() as cursor:
            # Проверяем, голосовал ли уже пользователь за эту инициативу
            cursor.execute(
                "SELECT vote_value FROM votes WHERE user_id = %s AND initiative_id = %s;",
                (session['user_id'], id)
            )
            existing_vote = cursor.fetchone()

            if existing_vote:
                # Если пользователь уже голосовал, сообщаем об этом
                flash('Вы уже проголосовали за эту инициативу', 'warning')
            else:
                # Если пользователь еще не голосовал, добавляем новый голос "За"
                cursor.execute(
                    "UPDATE initiatives SET votes = votes + 1 WHERE id = %s;",
                    (id,)
                )
                cursor.execute(
                    "INSERT INTO votes (user_id, initiative_id, vote_value) VALUES (%s, %s, 1);",
                    (session['user_id'], id)
                )
                flash('Ваш голос "За" учтен', 'success')

            conn.commit()  # Завершаем транзакцию
    except Exception as e:
        conn.rollback()  # Откатываем транзакцию в случае ошибки
        flash(f'Ошибка: {e}', 'danger')
    
    return redirect('/rgz')

@rgz.route('/rgz/vote/down/<int:id>', methods=['POST'])
def vote_down(id):
    if 'user_id' not in session:
        return redirect('/rgz/login')
    
    try:
        with conn.cursor() as cursor:
            # Проверяем, голосовал ли уже пользователь за эту инициативу
            cursor.execute(
                "SELECT vote_value FROM votes WHERE user_id = %s AND initiative_id = %s;",
                (session['user_id'], id)
            )
            existing_vote = cursor.fetchone()

            if existing_vote:
                # Если пользователь уже голосовал, сообщаем об этом
                flash('Вы уже проголосовали за эту инициативу', 'warning')
            else:
                # Если пользователь еще не голосовал, добавляем новый голос "Против"
                cursor.execute(
                    "UPDATE initiatives SET votes = votes - 1 WHERE id = %s;",
                    (id,)
                )
                cursor.execute(
                    "INSERT INTO votes (user_id, initiative_id, vote_value) VALUES (%s, %s, -1);",
                    (session['user_id'], id)
                )
                flash('Ваш голос "Против" учтен', 'success')

            conn.commit()  # Завершаем транзакцию
    except Exception as e:
        conn.rollback()  # Откатываем транзакцию в случае ошибки
        flash(f'Ошибка: {e}', 'danger')
    
    return redirect('/rgz')

@rgz.route('/rgz/delete/<int:id>', methods=['POST'])
def delete_initiativevb(id):
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему, чтобы удалить инициативу', 'danger')
        return redirect(url_for('rgz.loginn'))

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT user_id FROM initiatives WHERE id = %s;", (id,))
            initiative = cursor.fetchone()

            if not initiative:
                flash('Инициатива не найдена', 'danger')
                return redirect(url_for('rgz.indexx'))

            if session['user_id'] != initiative['user_id'] and not session.get('is_admin', False):
                flash('Вы не можете удалить эту инициативу', 'danger')
                return redirect(url_for('rgz.indexx'))

            cursor.execute("DELETE FROM votes WHERE initiative_id = %s;", (id,))
            cursor.execute("DELETE FROM initiatives WHERE id = %s;", (id,))
            conn.commit()
            flash('Инициатива успешно удалена', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Ошибка при удалении инициативы: {e}', 'danger')
    
    return redirect(url_for('rgz.indexx'))


@rgz.route('/rgz/admin/users')
def admin_users():
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('rgz.indexx'))

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            conn.commit()
    except Exception as e:
        conn.rollback()
        flash(f'Ошибка: {e}', 'danger')
        users = []

    return render_template('rgz/admin_users.html', users=users)

@rgz.route('/rgz/admin/users/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit_user(id):
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('rgz.indexx'))

    if request.method == 'POST':
        username = request.form.get('username')
        is_admin = request.form.get('is_admin') == 'on'

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET username = %s, is_admin = %s WHERE id = %s;",
                    (username, is_admin, id)
                )
                conn.commit()
                flash('Пользователь успешно обновлен', 'success')
                return redirect(url_for('rgz.admin_users'))
        except Exception as e:
            conn.rollback()
            flash(f'Ошибка: {e}', 'danger')

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s;", (id,))
            user = cursor.fetchone()
            conn.commit()
    except Exception as e:
        conn.rollback()
        flash(f'Ошибка: {e}', 'danger')
        user = None

    return render_template('rgz/admin_edit_user.html', user=user)

@rgz.route('/rgz/admin/users/delete/<int:id>', methods=['POST'])
def admin_delete_user(id):
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('rgz.indexx'))

    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s;", (id,))
            conn.commit()
            flash('Пользователь успешно удален', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Ошибка: {e}', 'danger')

    return redirect(url_for('rgz.admin_users'))


@rgz.route('/rgz/admin/initiatives/delete/<int:id>', methods=['POST'])
def admin_delete_initiative(id):
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('rgz.indexx'))

    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM initiatives WHERE id = %s;", (id,))
            conn.commit()
            flash('Инициатива успешно удалена', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Ошибка: {e}', 'danger')

    return redirect(url_for('rgz.indexx'))
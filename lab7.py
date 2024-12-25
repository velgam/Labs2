from flask import Blueprint, render_template, request, redirect, session, current_app, jsonify
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

films = [
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Энди Дюфрейн, успешный банкир, оказывается в тюрьме Шоушенк по обвинению в убийстве своей жены и ее любовника. Несмотря на несправедливость приговора, он не теряет надежду и находит дружбу в лице заключенного по имени Ред. Фильм рассказывает о силе духа, дружбе и надежде на свободу."
    },
    {
        "title": "Inception",
         "title_ru": "Начало",
        "year": 2010,
        "description": "Дом Кобб – талантливый вор, лучший из лучших в опасном искусстве извлечения: он крадет ценные секреты из глубин подсознания во время сна, когда человеческий разум наиболее уязвим. Коббу предлагают шанс вернуть все, что он потерял, но для этого он должен выполнить невозможное – внедрить идею в сознание другого человека."
    },
    {
        "title": "The Pursuit of Happyness",
        "title_ru": "В погоне за счастьем",
        "year": 2006,
        "description": "Крис Гарднер – отец-одиночка, который изо всех сил пытается обеспечить своего сына. Несмотря на бездомность и финансовые трудности, он устраивается на неоплачиваемую стажировку в брокерскую фирму, надеясь на лучшее будущее. Его история – это вдохновляющий пример упорства и веры в себя."
    },
]

@lab7.route('/lab7/')
def main():
    return render_template("lab7/index.html")

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_all_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_films(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404
    
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404
    del films[id]
    return "", 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404
    
    film = request.get_json()
    
    errors = {}
    if 'title_ru' not in film or not film['title_ru']:
        if 'title' not in film or not film['title']:
            errors['title'] = 'Название на оригинальном языке должно быть непустым, если русское название пустое'
    if 'title' not in film or not film['title']:
        if 'title_ru' not in film or not film['title_ru']:
            errors['title'] = 'Название на оригинальном языке должно быть непустым, если русское название пустое'
    if 'year' not in film:
        errors['year'] = 'Год должен быть указан'
    else:
        try:
            year = int(film['year'])  
            if not (1895 <= year <= datetime.now().year):
                errors['year'] = f'Год должен быть от 1895 до {datetime.now().year}'
        except ValueError:
            errors['year'] = 'Год должен быть числом'
    if 'description' not in film or not film['description']:
        errors['description'] = 'Описание должно быть непустым'
    if 'description' in film and len(film['description']) > 2000:
        errors['description'] = 'Описание должно быть не более 2000 символов'
    
    if errors:
        return jsonify(errors), 400
    
    if not film['title']:
        film['title'] = film['title_ru']
    
    films[id] = film
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    new_film = request.get_json()
    
    errors = {}
    if 'title_ru' not in new_film or not new_film['title_ru']:
        if 'title' not in new_film or not new_film['title']:
            errors['title'] = 'Название на оригинальном языке должно быть непустым, если русское название пустое'
    if 'title' not in new_film or not new_film['title']:
        if 'title_ru' not in new_film or not new_film['title_ru']:
            errors['title'] = 'Название на оригинальном языке должно быть непустым, если русское название пустое'
    if 'year' not in new_film:
        errors['year'] = 'Год должен быть указан'
    else:
        try:
            year = int(new_film['year'])  
            if not (1895 <= year <= datetime.now().year):
                errors['year'] = f'Год должен быть от 1895 до {datetime.now().year}'
        except ValueError:
            errors['year'] = 'Год должен быть числом'
    if 'description' not in new_film or not new_film['description']:
        errors['description'] = 'Описание должно быть непустым'
    if 'description' in new_film and len(new_film['description']) > 2000:
        errors['description'] = 'Описание должно быть не более 2000 символов'
    
    if errors:
        return jsonify(errors), 400
    
    if not new_film['title']:
        new_film['title'] = new_film['title_ru']
    
    films.append(new_film)
    
    new_film_index = len(films) - 1
    
    return jsonify({"id": new_film_index}), 201
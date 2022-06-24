from flask import Flask, jsonify
from utils import *

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def main_page():

    return "Работа с SQLite3, SQL-запросы, БД 'netflix.db'"


@app.route("/movie/<title>")
def get_page_movies_by_title(title):
    """Возвращает фильмы по title"""
    result = get_search_by_title(title)
    return jsonify(result)


@app.route("/movie/<year_1>/to/<year_2>")
def get_page_movies_by_year_range(year_1, year_2):
    """Возвращает фильмы по диапазону лет выпуска"""
    result = get_search_by_year_range(year_1, year_2)
    return jsonify(result)


@app.route("/rating/<age_rating>")
def get_page_movies_by_age_category(age_rating):
    """Возвращает фильмы по возрастной категории"""
    result = get_search_by_age_category(age_rating)
    return jsonify(result)


@app.route("/genre/<genre>")
def get_page_movies_by_genre(genre):
    """Возвращает фильмы по жанру"""
    genre = genre.lower()
    result = get_search_by_genre(genre)
    return jsonify(result)


@app.route("/cast/<actor_1>/and/<actor_2>")
def get_page_movies_by_actors(actor_1, actor_2):
    """Возвращает список тех актёров, кто играет с ними в паре больше 2 раз"""
    result = get_search_by_actors(actor_1, actor_2)
    return jsonify(result)


@app.route("/video/<video_type>/<year>/<genre>")
def get_page_movies_by_video_type(video_type, year, genre):
    """Возвращает видео по типу картины, году выпуска, жанру"""
    result = get_search_by_video_type(video_type, year, genre)
    return jsonify(result)


@app.errorhandler(404)
def page_not_found(e):
    return 'Страница не найдена :('


@app.errorhandler(500)
def server_error(e):
    return 'Ведутся технические работы...'


if __name__ == "__main__":
    app.run(debug=True)

import sqlite3
from collections import Counter  # Counter — это подкласс dict, который используется для подсчета объектов hashable


class ConnectData:
    """Подключение к БД"""

    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()


def get_search_by_title(title):
    """Возвращает фильмы по title"""
    data_connect = ConnectData('netflix.db')
    try:
        query = f"""
                    SELECT title, country, release_year, listed_in, description
                    FROM netflix
                    WHERE title LIKE '%{title}%'
                    ORDER BY release_year DESC 
                    """

        data_connect.cursor.execute(query)
        result = data_connect.cursor.fetchone()  # fetchone() - выводит один результат
        dict_result = {
            "title": result[0],
            "country": result[1],
            "release_year": result[2],
            "genre": result[3],
            "description": result[4]
        }
    except TypeError:
        return f"В БД нет фильмов по введённому запросу - '{title}'"

    return dict_result


def get_search_by_year_range(year_1, year_2):
    """Возвращает фильмы по диапазону лет выпуска"""
    data_connect = ConnectData('netflix.db')
    query = f"""
                    SELECT title, release_year
                    FROM netflix
                    WHERE release_year BETWEEN {year_1} AND {year_2}
                    ORDER BY release_year
                    LIMIT 100 
                    """
    data_connect.cursor.execute(query)
    result = data_connect.cursor.fetchall()
    list_result = []
    for data in result:
        list_result.append({"title": data[0],
                            "release_year": data[1]
                            })
    if len(list_result) > 0:
        return list_result
    else:
        return f"По введённому диапазону лет '{year_1} - {year_2}' в БД нет video"


def get_search_by_age_category(category):
    """Возвращает фильмы по возрастной категории"""

    age_categories = {"children": "'G'",
                      "family": "'G', 'PG', 'PG-13'",
                      "adult": "'R', 'NC-17'"
                      }
    data_connect = ConnectData('netflix.db')
    try:
        query = f"""
                                SELECT title, rating, description
                                FROM netflix
                                WHERE rating IN ({age_categories[category]}) 
                                ORDER BY rating
                                """

        data_connect.cursor.execute(query)
        result = data_connect.cursor.fetchall()
        list_result = []
        for data in result:
            list_result.append({"title": data[0],
                                "rating": data[1],
                                "description": data[2]
                                })
    except KeyError:
        return f"Возрастная категория '{category}' отсутствует в БД"

    return list_result


def get_search_by_genre(genre):
    """Возвращает фильмы по жанру"""
    data_connect = ConnectData('netflix.db')
    query = f"""
                        SELECT title, description
                        FROM netflix
                        WHERE listed_in LIKE '%{genre}%'
                        ORDER BY release_year DESC 
                        LIMIT 10
                        """
    data_connect.cursor.execute(query)
    result = data_connect.cursor.fetchall()
    list_result = []
    for data in result:
        list_result.append({"title": data[0],
                            "description": data[1]
                            })
    if len(list_result) > 0:
        return list_result
    else:
        return f"Video с жанром '{genre}' нет в БД '"


def get_search_by_actors(actor_1, actor_2):
    """Возвращает список тех актёров, кто играет с ними в паре больше 2 раз"""
    data_connect = ConnectData('netflix.db')
    query = f"""
                            SELECT `cast`
                            FROM netflix
                            WHERE `cast` LIKE '%{actor_1}%'
                            AND `cast` LIKE '%{actor_2}%'
                            """
    result = data_connect.cursor.execute(query)
    list_actors = []
    for data in result:
        list_actors.extend(data[0].split(', '))
    counter = Counter(list_actors)
    list_result = []
    for actor, count in counter.items():
        if actor not in [actor_1, actor_2] and count > 2:
            list_result.append(actor)

    if len(list_result) > 0:
        return list_result
    else:
        return f"В БД отсутствует результат, удовлетворяющий запросу - '{actor_1}, {actor_2}'"


def get_search_by_video_type(video_type, year, genre):
    """Возвращает видео по типу картины, году выпуска, жанру"""
    data_connect = ConnectData('netflix.db')
    query = f"""
                SELECT `type`, release_year, listed_in
                FROM netflix
                WHERE `type` LIKE '%{video_type}%'
                AND release_year LIKE '{year}'
                AND listed_in LIKE '%{genre}%'
                ORDER BY release_year
                """
    result = data_connect.cursor.execute(query)
    results = result.fetchall()
    list_result = []
    for data in results:
        list_result.append(
            {
                "type": data[0],
                "release_year": data[1],
                "genre": data[2]
            })

    if len(list_result) > 0:
        return list_result
    else:
        return f"В БД нет video по введённому запросу - '{video_type}, {year}, {genre}'"


# dc = ConnectData('netflix.db')
# print(dc)
# print(get_search_by_title('hello'))
# print(get_search_by_year_range('1950', '1945'))
# print(get_search_by_age_category("family"))
# print(get_search_by_genre("kids"))
# print(get_search_by_actors("Jack Black", "Dustin Hoffman"))
# print(get_search_by_video_type("Movie", "2020", "Horror"))

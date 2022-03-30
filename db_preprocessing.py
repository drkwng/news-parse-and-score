# TODO: preprocess cat_seen and add to db
# TODO: get check avail website and add to db

import json
from db_conn.db import MongoConnect


def modify_cat_seen(data):
    """
    Preprocess not unique websites and merge 'cat_seen' data.
    Finally make a list of dicts to dump data into db
    :param data:
    :type data: dict
    :return:
    :rtype:
    """

    # Merge not unique websites cat_seen values by website URL into dict
    final_data = {}
    for elem in data:
        if elem not in final_data.keys():
            final_data[elem] = {
                'name': elem['name'],
                'geo': [elem['geo']],
                'cat_seen': elem['cat_seen']
            }
        else:
            final_data[elem]['cat_seen'].append(elem['cat_seen'])

    # Make a list of dicts
    result = []
    for key, value in final_data.items():
        result.append(
            {
                'website': key,
                'name': value['name'],
                'geo': value['geo'],
                'cat_seen': value['cat_seen']
            }
        )
    return result


if __name__ == "__main__":
    host = 'localhost'
    port = '27017'
    db = 'news_websites'
    # collection = 'all_websites'
    collection = 'unique_websites'

    db_connect = MongoConnect(host, port, db, collection)
    # db_connect.dump_db()

    # db_connect2.insert_many(MY_JSON)

    dump_file = 'website_data.json'
    with open(dump_file) as f:
        data = json.load(f)

    # TODO: Запустить функцию препроцессинга и записать в базу
    #  После делаем запись в базу отдельную (уники)
    # TODO: Проверяем доступность сайтов и пишем в базу

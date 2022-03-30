# TODO: preprocess cat_seen and add to db
# TODO: get check avail website and add to db

import json

from concurrent.futures import ThreadPoolExecutor

from db_conn.db import MongoConnect
from parser_feedspot.parser import ParserFeedspot


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
        if elem['website'] not in final_data.keys():
            final_data[elem['website']] = {
                'name': elem['name'],
                'geo': elem['geo'],
                'cat_seen': [elem['cat_seen']]
            }
        else:
            final_data[elem['website']]['cat_seen'].append(elem['cat_seen'])

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

    dump_file = 'website_data.json'
    with open(dump_file) as f:
        data = json.load(f)

    # Check website availability
    prepro_data = modify_cat_seen(data)
    print(f'Websites left: {len(prepro_data)} of {len(data)}')

    parser = ParserFeedspot()
    print('Start checking websites availability. Please, wait...')
    with ThreadPoolExecutor(max_workers=100) as executor:
        for item in prepro_data:
            item['available'] = executor.submit(parser.check_avail_website,
                                                item['website']).result()
            print(f"{item['website']} checked")

    # Add received data to the DB and dump into JSON
    db_connect.insert_many(prepro_data)
    db_connect.dump_db(filename='website_data_final.json')

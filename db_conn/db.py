
import pymongo

from bson.json_util import dumps
import json

import logging


def update_db(host, port, data):
    """
    Update DB
    :param host: Hostname (e.g. localhost)
    :type host: str
    :param port: Port (e.g. 27017)
    :type port: str
    :param data:
    :type data: dict
    :return:
    :rtype:
    """
    try:
        client = pymongo.MongoClient(f'mongodb://{host}:{port}/')

        db = client.admin
        city = db.cities

        city_id = city.insert_one(data).inserted_id
        logging.info(f"Success! City {data['city']} added, id {city_id}")

    except Exception as err:
        logging.debug('db update_db() func error: ', err)


def dump_db(host, port):
    """
    Dump DB data into JSON
    :param host: Hostname (e.g. localhost)
    :type host: str
    :param port: Port (e.g. 27017)
    :type port: str
    :return:
    :rtype:
    """
    try:
        client = pymongo.MongoClient(f'mongodb://{host}:{port}/')
        db = client.admin
        collection = db.cities
        cursor = collection.find({})
        with open('city_data.json', 'w') as file:
            json.dump(json.loads(dumps(cursor)), file)
        print('Dump succeed!')

    except Exception as err:
        logging.debug('db dump_db() func error: ', err)


if __name__ == "__main__":
    test_data = {
        'field1': 'value1',
        'field2': 'value2',
        'field3': ['val1', 'val2', 'val3']
    }

    update_db('localhost', '27017', test_data)

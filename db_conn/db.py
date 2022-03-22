import logging

import pymongo
from bson.json_util import dumps
import json


class MongoConnect:
    def __init__(self, _host, _port, database, collection):
        client = pymongo.MongoClient(f'mongodb://{_host}:{_port}/')
        db = client[database]
        self.collection = db[collection]

    def send_to_db(self, data):
        """
        Insert new data into MongoDB collection
        :param data:
        :type data: dict
        :return:
        :rtype:
        """
        try:
            self.collection.insert_one(data).inserted_id

        except Exception as err:
            logging.debug('db send_to_db() func error: ', err)

    def dump_db(self):
        """
        Makes JSON dump of MongoDB collection
        :return:
        :rtype:
        """
        try:
            cursor = self.collection.find({})
            with open('website_data.json', 'w') as file:
                result = json.loads(dumps(cursor))
                json.dump(result, file)
            print('Dump succeed!')
            return result

        except Exception as err:
            logging.debug('db dump_db() func error: ', err)

    def worker(self, cor):
        """
        Gets parser worker coroutine and sends data into database
        :param cor: coroutine
        :type cor: generator
        :return:
        :rtype:
        """
        for data in cor:
            for elem in data:
                self.send_to_db(elem)

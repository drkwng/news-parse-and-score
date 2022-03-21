import logging

import pymongo
from bson.json_util import dumps
import json

from parser_feedspot.parser import ParserFeedspot


class MongoConnect:
    def __init__(self, _host, _port):
        client = pymongo.MongoClient(f'mongodb://{_host}:{_port}/')
        db = client.admin
        self.website = db.websites

    def send_to_db(self, data):
        try:
            self.website.insert_one(data).inserted_id

        except Exception as err:
            logging.debug('db send_to_db() func error: ', err)

    def dump_db(self):
        try:
            cursor = self.website.find({})
            with open('website_data.json', 'w') as file:
                json.dump(json.loads(dumps(cursor)), file)
            print('Dump succeed!')

        except Exception as err:
            logging.debug('db dump_db() func error: ', err)

    def worker(self, cor):
        for data in cor:
            for elem in data:
                self.send_to_db(elem)


if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', filemode='w', level=logging.DEBUG)

    start_url = "https://blog.feedspot.com/category/usa-news-websites/"

    host = 'localhost'
    port = '27017'
    db_connect = MongoConnect(host, port)

    parser = ParserFeedspot()
    parse_worker = parser.worker(start_url)

    db_connect.worker(parse_worker)
    db_connect.dump_db()


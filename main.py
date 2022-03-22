import logging

from db_conn.db import MongoConnect
from parser_feedspot.parser import ParserFeedspot


if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', filemode='w', level=logging.DEBUG)

    start_url = "https://blog.feedspot.com/category/usa-news-websites/"

    host = 'localhost'
    port = '27017'
    db = 'news_websites'
    collection = 'all_websites'
    db_connect = MongoConnect(host, port, db, collection)

    parser = ParserFeedspot()
    parse_worker = parser.worker(start_url)
    db_connect.worker(parse_worker)

    # Dump data
    db_connect.dump_db()


import logging

from db_conn.db import MongoConnect
from parser_feedspot.parser import ParserFeedspot
from parser_feedspot.valueserp import SerpAPI


def unique_websites(_data):
    unique_data = [list({value['website']: value for value in _data}.values())]
    for elem in unique_data[0]:
        del elem['_id']
    return unique_data[0]


def main():
    start_url = "https://blog.feedspot.com/category/usa-news-websites/"

    host = 'localhost'
    port = '27017'
    db = 'news_websites'
    collection = 'all_websites'
    collection2 = 'unique_websites'
    collection3 = 'websites_with_serp_data'
    db_connect = MongoConnect(host, port, db, collection)
    db_connect2 = MongoConnect(host, port, db, collection2)
    db_connect3 = MongoConnect(host, port, db, collection3)

    parser = ParserFeedspot()
    parse_worker = parser.worker(start_url)
    db_connect.worker(parse_worker)

    print('Parse done! Starting DB website duplicates cleaning')

    # Dump data from MongoDB and unique websites
    dump_data = db_connect.dump_db()
    db_connect2.insert_many(unique_websites(dump_data))

    dump_data = db_connect2.dump_db(dump_file='no')
    input(f'\nDone! Starting scraping data via Value SERP API\n'
          f'Please check that you have enough limits and press Enter\n'
          f'There are {len(dump_data)} websites to check\n')
    print(dump_data)

    # Value SERP parser
    # api_key = '68375F40DAB2479E9678F9EAB68E18B0'
    # search_type = 'news'
    # location = 'United States'
    #
    # query = input('Please enter the keyword you want to scrape websites data: \n').strip()
    #
    # init_api = SerpAPI(api_key, search_type, location)
    #
    # print('Start getting data from Value SERP API. Please wait...\n')
    #
    # api_worker = init_api.worker(dump_data, query)
    # for elem in api_worker:
    #     del elem['_id']
    #     db_connect3.insert_one(elem)
    #
    # db_connect3.dump_db()
    # print(f'Done! Check the DB: {db}, Collection: {collection3}\n'
    #       f'Also, there is a dump in websites_data.json file')


if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', filemode='w', level=logging.DEBUG)

    main()

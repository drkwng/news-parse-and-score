import logging

from queue import Queue
import requests


class SerpAPI:
    def __init__(self, _api_key, _search_type, _location):
        """
        https://www.valueserp.com/docs/search-api/searches/common
        :param _api_key: API Key
        :type _api_key: str
        :param _search_type: optional (e.g. 'news')
        :type _search_type: str
        :param _location: optional (e.g. 'United States')
        :type _location: str
        """
        self.api_key = _api_key
        self.search_type = _search_type
        self.location = _location
        self.q = Queue()

    def get_search_data(self, _query):
        """
        Send request to Value SERP API
        :param _query:
        :type _query:
        :return:
        :rtype: dict
        """
        try:
            params = {
                'api_key': self.api_key,
                'q': _query,
                'search_type': self.search_type,
                'location': self.location
            }
            api_result = requests.get('https://api.valueserp.com/search', params)
            return api_result.json()

        except Exception as err:
            logging.debug(f'get_search_data({query}): {err}')
            return None

    def worker(self, _data, _query):
        """
        :param _data: JSON dump from database
        :type _data: dict
        :param _query: keyword
        :type _query: str
        :return: Dict element with serp data
        :rtype: generator
        """
        self.q.put(_data)

        while not self.q.empty():
            element = self.q.get()
            website = element['website']
            serp_data = self.get_search_data(
                f'site:{website} {_query}')
            element['serp_data'] = {
                query: serp_data
            }
            print(f'{website} - checked')
            # Return scraped data to send it to db
            yield element


if __name__ == "__main__":
    api_key = '68375F40DAB2479E9678F9EAB68E18B0'
    search_type = 'news'
    location = 'United States'

    data = {
        "_id": {"$oid": "6239a9a6a51aec6e8d8d1462"},
        "name": "CNN - Breaking News, Latest News and Videos",
        "website": "https://us.cnn.com/",
        "geo": "US",
        "cat_seen": "USA",
        "available": True
    }
    query = 'ukraine'

    init_api = SerpAPI(api_key, search_type, location)
    print([work for work in init_api.worker(data, query)])

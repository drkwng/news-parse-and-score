import requests


class SerpAPI:
    def __init__(self, key):
        self.key = key

    def get_search_data(self, url, keyword)
        query = f"site:url keyword"
        params = {
            'api_key': self.key,
            'q': query,
            'search_type': 'news'
        }


if __name__ == "__main__":
    url = 'https://us.cnn.com/'

    import requests

    # set up the request parameters
    params = {
        'api_key': 'demo',
        'q': 'pizza'
    }

    # make the http GET request to VALUE SERP
    api_result = requests.get('https://api.valueserp.com/search', params)

    # print the JSON response from VALUE SERP
    print(api_result.json())

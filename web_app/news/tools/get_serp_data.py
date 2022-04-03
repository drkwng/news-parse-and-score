import requests

from queue import Queue

from super_news.settings import SERP_API
from news.models import Website, Query, QueryCheck


def preprocess_data(data):
    """
    Preprocess data from list of dicts (JSON response) and make it plain text
    """
    serp_text = ""
    try:
        for elem in data['news_results']:
            serp_text += f"<div class='item'>" \
                         f"<span class='item_title'>{elem['title']}</span>" \
                         f"<span class='item_snippet'>{elem['snippet']}</span>" \
                         f"<span class='item_time'>{elem['date_utc'].split('T')}</span>" \
                         f"</div>"
    except Exception as err:
        print(f'Preprocess {data} error: {err}')
    finally:
        return serp_text


def get_serp_data(query, location):
    """
    Make API request
    """
    try:
        params = {
            'api_key': SERP_API,
            'q': query,
            'search_type': 'news',
            'location': location
        }
        api_response = requests.get('https://api.valueserp.com/search', params)
        return api_response.json()
    except Exception as err:
        print(f'Get {query} SERP Data error: {err}')
        return None


def update_db(url, keyword, serp_data):
    """
    Add results to Database
    """
    website = Website.objects.get(url=url)
    query = Query.objects.get(query=keyword)
    data = QueryCheck(
        query=query,
        website=website,
        serp_data=serp_data
    )
    data.save()


def run(url, keyword, location):

    query = f'site:{url} {keyword}'

    response = get_serp_data(query, location)
    raw_text = preprocess_data(response)
    update_db(url, keyword, raw_text)

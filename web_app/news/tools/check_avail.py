from requests import Session
from fake_useragent import UserAgent

from news.models import Website


def check_website(url):
    """
    Check website availability by a HTTP status code. If 400+ then not available.
    """
    user_agent = {'user-agent': UserAgent().chrome}
    try:
        with Session() as session:
            response = session.get(url, headers=user_agent, timeout=3)
            if response.status_code < 400:
                return True
            else:
                return False
    except Exception as err:
        return False


def update_db(url, result):
    try:
        Website.objects.filter(url=url).update(available=result)
    except Website.DoesNotExist:
        print(f'Website {url} does not added into DB')


def run(url):
    response = check_website(url)
    update_db(url, response)


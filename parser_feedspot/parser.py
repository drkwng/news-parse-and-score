
import logging

from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor


def crawl_list_dirs(url):
    with HTMLSession() as session:
        try:
            r = session.get(url)
            links = r.html.xpath("//table[@class='table']/*/tr/td/a/@href")
            abs_links = ['https://blog.feedspot.com' + link for link in links]
            return abs_links

        except Exception as err:
            logging.debug('crawl_list_dirs(): ', err)


def crawl_dir(url):
    with HTMLSession() as session:
        try:
            r = session.get(url)

            dir_name = r.html.xpath("//h2[@id='fsbhead']/text()")[0].strip(' News Websites')
            data = {
                'dir_name': dir_name,
                'dir_data': []
            }

            dir_list = r.html.xpath("//*[contains(@class, 'trow-wrap')]")

            for num, elem in enumerate(dir_list):
                name = elem.element.xpath("//a[@class='tlink']/text()")[num-1]
                website = elem.element.xpath("//a[@class='ext']/@href")[num-1]
                geo = elem.element.xpath("//span[@class='location_new']/text()")[num-1]

                data['dir_data'].append(
                    {
                        'name': name,
                        'website': website,
                        'geo': geo,
                    }
                )

            return data

        except Exception as err:
            logging.debug('crawl_dir(): ', err)


def worker():
    # TODO: Разово запускаємо скрипт на стартовий урл.
    #  Після проходимося по урл зі списку,
    #  доти на виході список не порожній,
    #  інакше запускаємо функцію краулінга каталогу
    pass


if __name__ == "__main__":
    from pprint import pprint

    # url = 'https://blog.feedspot.com/new_york_news_websites/'
    url = 'https://blog.feedspot.com/san_diego_news_websites/'

    # url = "https://blog.feedspot.com/category/usa-news-websites/"
    # crawl_list_dirs(url)

    dir_list = crawl_dir(url)
    pprint(dir_list)

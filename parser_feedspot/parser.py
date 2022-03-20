
import logging
from time import sleep
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from requests_html import HTMLSession


def crawl_list_dirs(url):
    with HTMLSession() as session:
        try:
            r = session.get(url)

            links = r.html.xpath("//table[@class='table']/*/tr/td/a/@href")
            abs_links = []
            for link in links:
                if 'https' not in link:
                    abs_links.append('https://blog.feedspot.com' + link)
                else:
                    abs_links.append(link)
            return abs_links

        except Exception as err:
            logging.debug('crawl_list_dirs(): ', err)


def scrape_list_dirs(url):
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
            print(data)
            return data

        except Exception as err:
            logging.debug('crawl_dir(): ', err)


def worker(start_url):
    q = Queue()
    [q.put(i) for i in crawl_list_dirs(start_url)]

    data = []

    while not q.empty():
        element = q.get()
        if '/category/' in element:
            [q.put(i) for i in crawl_list_dirs(element)]
            sleep(2)
        else:
            data.append(scrape_list_dirs(element))
            sleep(2)

    return data


if __name__ == "__main__":
    from pprint import pprint

    url = 'https://blog.feedspot.com/san_diego_news_websites/'
    # dir_list = scrape_list_dirs(url)
    # pprint(dir_list)

    start_url = "https://blog.feedspot.com/category/usa-news-websites/"
    worker(start_url)




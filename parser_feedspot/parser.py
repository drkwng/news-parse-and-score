from queue import Queue

from requests import Session
from fake_useragent import UserAgent
from lxml import etree

from random import randint
from time import sleep

import logging


class ParserFeedspot():
    def __init__(self):
        self.ua = {'user-agent': UserAgent().chrome}
        self.q = Queue()

    def crawl_list_dirs(self, url):
        # TODO: Check if there is button show more (JS code + render)

        try:
            with Session() as session:
                response = session.get(url, headers=self.ua)
                html_code = response.content

            tree = etree.HTML(html_code)
            links = tree.xpath("//table[@class='table']/*/tr/td/a/@href")
            for link in links:
                if 'https' not in link:
                    self.q.put('https://blog.feedspot.com' + link)
                else:
                    self.q.put(link)
            return self.q

        except Exception as err:
            logging.debug('crawl_list_dirs(): ', err)

    def scrape_list_dirs(self, url):
        try:
            with Session() as session:
                response = session.get(url, headers=self.ua)
                html_code = response.content
                tree = etree.HTML(html_code)

            dir_name = tree.xpath("//h2[@id='fsbhead']/text()")[0].strip(' News Websites')

            data = []

            dir_list = tree.xpath("//*[contains(@class, 'trow-wrap')]")
            for num, elem in enumerate(dir_list):
                name = elem.xpath(f"(//a[@class='tlink']/text())[{num-1}]")[0]
                website = elem.xpath(f"(//a[@class='ext']/@href)[{num-1}]")[0]
                geo = elem.xpath(f"(//span[@class='location_new']/text())[{num-1}]")[0]

                data.append(
                    {
                        'name': name,
                        'website': website,
                        'geo': geo,
                        'cat_seen': dir_name
                    }
                )
            return data

        except Exception as err:
            logging.debug('srape_dir_list(): ', err)

    def worker(self, start_url):
        self.crawl_list_dirs(start_url)

        while not self.q.empty():
            element = self.q.get()
            print(f'{element} | {self.q.qsize()} left')

            if '/category/' in element:
                self.crawl_list_dirs(element)
            else:
                data = self.scrape_list_dirs(element)
                yield data
            sleep(randint(2, 4))


if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', filemode='w', level=logging.DEBUG)

    start_url = "https://blog.feedspot.com/category/usa-news-websites/"

    parser = ParserFeedspot()
    print([work for work in parser.worker(start_url)])

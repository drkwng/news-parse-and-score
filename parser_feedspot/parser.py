from queue import Queue

from requests import Session
from fake_useragent import UserAgent
from lxml import etree

from concurrent.futures import ThreadPoolExecutor

from random import randint
from time import sleep

import logging


class ParserFeedspot:
    def __init__(self):
        self.ua = {'user-agent': UserAgent().chrome}
        self.q = Queue()

    def crawl_list_dirs(self, url):
        """
        Crawls category URLs and adds found URLs into queue
        :param url:
        :type url: str
        :return:
        :rtype: queue.Queue
        """

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
            logging.debug(f'crawl_list_dirs({url}): {err}')

    def scrape_websites(self, url):
        """
        Scrapes each website data from directory by URL
        :param url:
        :type url: str
        :return: list where each element is a dict with website data
        :rtype: list
        """
        try:
            with Session() as session:
                response = session.get(url, headers=self.ua)
                html_code = response.content
                tree = etree.HTML(html_code)

            dir_name = tree.xpath("//h2[@id='fsbhead']/text()")[0].strip(' News Websites')

            data = []

            dir_list = tree.xpath("//*[contains(@class, 'trow-wrap')]")
            for num, elem in enumerate(dir_list):
                # Check on empty elements (hidden)
                if len(elem.xpath(f"(//a[@class='tlink']/text())[{num-1}]")) > 0:
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
            logging.debug(f'srape_dir_list({url}): {err}')

    def check_avail_website(self, url):
        """
        Check if website has status 200 code
        :param url:
        :type url: str
        :return:
        :rtype: bool
        """
        try:
            with Session() as session:
                response = session.get(url, headers=self.ua, timeout=5)
                if response.status_code < 400:
                    return True
                else:
                    return False

        except Exception as err:
            logging.debug(f'check_avail_website({url}): {err}')
            return False

    def worker(self, start_url):
        # fill the queue first time
        self.crawl_list_dirs(start_url)

        while not self.q.empty():
            element = self.q.get()
            print(f'{element} | {self.q.qsize()} left')

            if '/category/' in element:
                self.crawl_list_dirs(element)
            else:
                data = self.scrape_websites(element)

                # Check availability of websites
                with ThreadPoolExecutor(max_workers=30) as executor:
                    for item in data:
                        item['available'] = executor.submit(self.check_avail_website,
                                                            item['website']).result()

                yield data

            sleep(randint(2, 4))


if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', filemode='w', level=logging.DEBUG)

    start_url = "https://blog.feedspot.com/category/usa-news-websites/"

    parser = ParserFeedspot()
    print([work for work in parser.worker(start_url)])

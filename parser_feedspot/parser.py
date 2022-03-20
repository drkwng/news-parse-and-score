
import logging
from time import sleep

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
    to_crawl = crawl_list_dirs(start_url)
    data = []

    while len(to_crawl) > 0:
        for element in to_crawl:
            if '/category/' in element:
                print(f'crawl - {element}')
                to_crawl += crawl_list_dirs(element)
                to_crawl.remove(element)
                print(f'{len(to_crawl)} left')
                sleep(2)

            else:
                print(f'scrape - {element}')
                data.append(scrape_list_dirs(element))
                to_crawl.remove(element)
                print(f'{len(to_crawl)} left')
                sleep(2)

    return data


if __name__ == "__main__":
    from pprint import pprint

    # url = 'https://blog.feedspot.com/new_york_news_websites/'
    url = 'https://blog.feedspot.com/san_diego_news_websites/'
    # dir_list = scrape_list_dirs(url)
    # pprint(dir_list)

    # start_url = "https://blog.feedspot.com/category/usa-news-websites/"
    start_url = 'https://blog.feedspot.com/category/california-news-websites?_src=categorypage'
    # pprint(crawl_list_dirs(start_url))

    worker(start_url)




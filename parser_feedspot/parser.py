
import logging
from requests_html import HTMLSession


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
            for elem in dir_list:
                website = elem.xpath("//a[@class='ext']/@href")[0]
                geo = elem.xpath("//span[@class='location_new']/text()")[0].split(',')[0]
                metrics = []

                data['dir_data'].append(
                    {
                        'website': website,
                        'geo': geo,
                        'metrics': metrics
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
    # url = 'https://blog.feedspot.com/new_york_news_websites/'
    url = 'https://blog.feedspot.com/san_diego_news_websites/'

    # url = "https://blog.feedspot.com/category/usa-news-websites/"
    # crawl_list_dirs(url)

    data = crawl_dir(url)
    print(data)

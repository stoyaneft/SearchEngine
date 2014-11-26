import requests
import urllib
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from page import Page
from website import Website
from connections import *


class Spider():

    def __init__(self, website, scan_depth=None):
        Base.metadata.create_all(engine)
        self.__session = Session()
        self.website = website
        self.domain = Spider.get_domain(website)
        self.scanned_urls = []
        self.website_info = self.get_website_info()
        self.pages_info = {}
        self.scan_depth = scan_depth

    @staticmethod
    def get_domain(url):
        parsed_uri = urlparse(url)
        base_url = '{uri.netloc}'.format(uri=parsed_uri)
        return base_url

    def get_website_info(self):
        r = requests.get(self.website)
        html = r.text
        soup = BeautifulSoup(html)
        info = {'url': self.website}
        info['title'] = soup.title.string if soup.title else None
        info['description'] = soup.description.string if soup.description else None
        info['pages_count'] = 0
        return info
        print(info)

    def get_page_info(self, soup):
        info = {}
        info['title'] = soup.title.string if soup.title else None
        info['description'] = soup.description.string if soup.description else None
        return info

    def is_outgoing(self, url):
        if '//' + self.domain in url or 'www.' + self.domain in url:
            return False
        return True

    def prepare_url(self, url, href):
        return urllib.parse.urljoin(url, href)

    def save_page_info(self, url, soup):
        page_info = self.get_page_info(soup)
        pages_count = self.website_info['pages_count']
        self.pages_info[pages_count] = page_info
        self.pages_info[pages_count]['url'] = url

    def scan_website(self, url):
        if url not in self.scanned_urls:
            print(url)
            self.scanned_urls.append(url)
            r = requests.get(url)
            html = r.text
            soup = BeautifulSoup(html)
            self.website_info['pages_count'] += 1
            self.save_page_info(url, soup)
            for link in soup.find_all('a'):
                new_link = self.prepare_url(url, link.get('href'))
                if not self.is_outgoing(new_link):
                    self.scan_website(new_link)
                if self.scan_depth:
                    if self.website_info['pages_count'] == self.scan_depth:
                        return

    def save_in_db(self):
        urls = [url[0] for url in self.__session.query(Page.url).all()]
        for page in self.pages_info.values():
            if page['url'] in urls:
                return
            pg = Page(**page)
            self.__session.add(pg)
        self.__session.commit()


def main():
    spider = Spider('http://hackbulgaria.com/', 5)
    spider.scan_website('http://hackbulgaria.com/')
    spider.save_in_db()
    print(spider.pages_info)

if __name__ == '__main__':
    main()

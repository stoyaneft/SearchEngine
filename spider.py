import requests
import urllib
from urllib.parse import urlparse
from connections import *

from bs4 import BeautifulSoup


class Spider():

    def __init__(self, website):
        Base.metadata.create_all(engine)
        self.__session = Session()
        self.website = website
        self.domain = Spider.get_domain(website)
        self.scanned_urls = []

    @staticmethod
    def get_domain(url):
        parsed_uri = urlparse(url)
        base_url = '{uri.netloc}'.format(uri=parsed_uri)
        return base_url

    def is_outgoing(self, url):
        if '//' + self.domain in url or 'www.' + self.domain in url:
            return False
        return True

    def prepare_url(self, url, href):
        return urllib.parse.urljoin(url, href)

    def scan_website(self, url):
        if url not in self.scanned_urls:
            print(url)
            self.scanned_urls.append(url)
            r = requests.get(url)
            html = r.text
            soup = BeautifulSoup(html)
            for link in soup.find_all('a'):
                new_link = self.prepare_url(url, link.get('href'))
                if not self.is_outgoing(new_link):
                    self.scan_website(new_link)


def main():
    spider = Spider('http://hackbulgaria.com/')
    spider.scan_website('http://hackbulgaria.com/')

if __name__ == '__main__':
    main()

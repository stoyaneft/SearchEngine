import requests
import urllib
from urllib.parse import urlparse
import re
import bs4
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
        self.to_scan = [website]

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
        info['pages_count'] = 0
        info['HTML_version'] = self.get_HTML_version()
        return info

    def get_page_info(self, soup):
        info = {}
        info['title'] = soup.title.string if soup.title else None
        description = soup.find(attrs={"property": "og:description"})
        if description:
            info['description'] = description['content'].encode('utf-8')
        return info

    def is_outgoing(self, url):
        if '//' + self.domain in url or 'www.' + self.domain in url:
            return False
        return True

    def prepare_url(self, url, href):
        return urllib.parse.urljoin(url, href)

    def get_HTML_version(self):
        soup = BeautifulSoup(requests.get(self.website).text)
        items = [
            item for item in soup.contents if isinstance(item, bs4.Doctype)]
        doctype = items[0] if items else None
        html_version = re.search(
            'HTML (?P<version>\d+.\d+)', doctype).group('version')
        return html_version

    def save_page_info(self, url, soup):
        page_info = self.get_page_info(soup)
        pages_count = self.website_info['pages_count']
        self.pages_info[pages_count] = page_info
        self.pages_info[pages_count]['url'] = url
        self.pages_info[pages_count]['website_url'] = self.website

    def should_be_scanned(self, url):
        return url not in self.scanned_urls \
            and not self.is_outgoing(url) and '#' not in url

    def scan_page(self, url):
        print(url)
        self.scanned_urls.append(url)
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html)
        self.website_info['pages_count'] += 1
        self.save_page_info(url, soup)
        for link in soup.find_all('a'):
            new_link = self.prepare_url(url, link.get('href'))
            if self.should_be_scanned(new_link):
                self.to_scan.append(new_link)

    def scan_website(self):
        while len(self.to_scan) != 0:
            self.scan_page(self.to_scan.pop())
            if self.scan_depth:
                if self.website_info['pages_count'] == self.scan_depth:
                    return

    def save_in_db(self):
        saved_urls = [url[0] for url in self.__session.query(Page.url).all()]
        for page in self.pages_info.values():
            if page['url'] in saved_urls:
                continue
            pg = Page(**page)
            self.__session.add(pg)
        saved_websites = [site[0]
                          for site in self.__session.query(Website.url).all()]
        if self.website not in saved_websites:
            self.__session.add(Website(**self.website_info))
        self.__session.commit()


def main():
    spider = Spider('https://www.mattcutts.com/blog/hermit-mode/')
    spider.scan_website()
    spider.save_in_db()

if __name__ == '__main__':
    main()

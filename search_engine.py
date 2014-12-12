from page import Page
from website import Website
from connections import *
from sqlalchemy import desc


class SearchEngine:

    def __init__(self):

        Base.metadata.create_all(engine)
        self.__session = Session()
        self.__session.commit()

    def calculate_points(self, keywords):
        pages = self.__session.query(Page).all()
        for page in pages:
            points = 0
            # points += page.website.pages_count
            for keyword in keywords:
                if page.title:
                    if keyword.lower() in page.title.lower():
                        points += 10
                if page.description:
                    if keyword.lower() in page.description.decode(
                            'utf-8').lower():
                        points += 5
            self.__session.query(Page).filter(
                Page.url == page.url).update({'points': points})
        self.__session.commit()

    def search(self, search_string):
        keywords = search_string.split(' ')
        self.calculate_points(keywords)
        result = self.__session.query(Page).filter(
            Page.points > 0).order_by(desc(Page.points)).all()
        self.__session.commit()
        return result

if __name__ == '__main__':
    print(SearchEngine().search('search'))

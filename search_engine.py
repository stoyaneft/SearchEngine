from connections import *


class SearchEngine:

    def __init__(self):
        Base.metadata.create_all(engine)
        self.__session = Session()



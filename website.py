from sqlalchemy import Column, Integer, String
from connections import *


class Website(Base):
    __tablename__ = "websites"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    pages_count = Column(Integer)
    HTML_version = Column(String)

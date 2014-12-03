from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from connections import *


class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Integer)
    url = Column(String)
    ssl = Column(Boolean)
    points = Column(Integer)
    website_url = Column(String, ForeignKey("websites.url"))
    website = relationship("Website", backref="pages")

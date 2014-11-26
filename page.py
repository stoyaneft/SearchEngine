from sqlalchemy import Column, Integer, String, Boolean
from connections import *


class Website(Base):
    __tablename__ = "websites"
    id = Column(Integer, primary_key=True)
    website = Column(String)
    title = Column(String)
    description = Column(Integer)
    url = Column(String)
    ssl = Column(Boolean)
    points = Column(Integer)

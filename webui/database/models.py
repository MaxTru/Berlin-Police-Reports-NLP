"""Models for the SQLAlchemy ORM Framework."""

from sqlalchemy import Column, Integer, String
from webui.database.db_setup import Base
import dateutil.parser as parser

class Report(Base):
    """Class represents a row in the reports table in the SQLite database."""
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    title = Column(String)
    link = Column(String)
    event = Column(String)
    location = Column(String)
    label = Column(String)

    def __init__(self, id=None, date=None, title=None, link=None, event=None, location=None, label=None):
        self.id = id
        self.date = date
        self.title = title
        self.link = link
        self.event = event
        self.location = location
        self.label = label

    def __repr__(self):
        return '<Event %r>' % (self.event)

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import generic_repr


Base = declarative_base()


@generic_repr
class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    page_title = Column(String(100))
    links_from = relationship('Link', back_populates='page_from')
    links_to = relationship('Link', back_populates='page_to')


@generic_repr
class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    page_from_fk = Column(Integer, ForeignKey('pages.id'))
    page_to_fk = Column(Integer, ForeignKey('pages.id'))
    page_from = relationship('Page', back_populates='links_from')
    page_to = relationship('Page', back_populates='links_to')

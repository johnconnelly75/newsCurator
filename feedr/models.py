__author__ = 'john'
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import config

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**config.DATABASE))


DeclarativeBase = declarative_base()



def create_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


# class Deals(DeclarativeBase):
#     """Sqlalchemy deals model"""
#     __tablename__ = "deals"
#
#     id = Column(Integer, primary_key=True)
#     title = Column('title', String)
#     link = Column('link', String, nullable=True)
#     location = Column('location', String, nullable=True)
#     original_price = Column('original_price', Integer, nullable=True)
#     price = Column('price', Integer, nullable=True)
#     end_date = Column('end_date', DateTime, nullable=True)


#################################################
##################### FEEDS #####################
#################################################




# class article(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(450))
#     summary = db.Column(db.String(1550))
#     link = db.Column(db.String(550))
#     source = db.Column(db.String(150))
#     published = db.Column(db.String(150))
#     timestamp = db.Column(db.DateTime)
#
#     parsed = db.Column(db.String(4)) #
#     # true if set to delete / rule could be if nuMention = False and 6 months from timestamp
#     delete = db.Column(db.String(4))
#     nuMention = db.Column(db.String(4)) # true if nu is mentioned in article
#
#
#     def __repr__(self):
#         return '<tag %r>' % (self.projectName)

class FeedSources(DeclarativeBase):
    """
    table of
    """
    __tablename__ = "feed_sources"
    id = Column(Integer, primary_key = True)
    name_ = Column('name_', String(150))
    url = Column('url', String(150))
    dateAdded = Column('date_added', String(150))
    nuMentions = Column('nu_mentions', Integer)

    def __repr__(self):
        return '<source %r>' % (self.name_)


class Feeds(DeclarativeBase):
    __tablename__ = "feeds"
    id = Column(Integer, primary_key = True)
    title = Column('title', String(450))
    summary = Column('summary', String(1550))
    rawSummary = Column('rawSummary', String(1550))
    link = Column('link', String(550))
    actualURL = Column('actualURL', String(550))
    source = Column('source', String(150))
    published = Column('published', String(150))
    timestamp = Column('timestamp', DateTime)

    parsed = Column('parsed_ind', String(4)) #
    # true if set to delete / rule could be if nuMention = False and 6 months from timestamp
    delete =  Column('delete_ind', String(4))
    nuMention =  Column('nu_mention', String(4)) # true if nu is mentioned in article

    source_id = Column('source_id', Integer, ForeignKey('feed_sources.id'))
    #user_id =  db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<feedTitle %r>' % (self.title)
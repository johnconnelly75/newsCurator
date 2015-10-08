__author__ = 'john'
from sqlalchemy.orm import sessionmaker
from models import FeedSources, Feeds, db_connect, create_tables


class NewsFeedPipeline(object):
    """News Feeds pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        self.engine = db_connect()
        create_tables(self.engine)
        self.Session = sessionmaker(bind=self.engine)


    def processDBentry(self, tblObj):
        session = self.Session()
        try:
            session.add(tblObj)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def process_source(self, item):
        """adds source in the database.
        """

        src = FeedSources(**item)
        self.processDBentry(src)
        return item

    def processFeedItem(self, item):
        """
        adds news item to feeds table
        :param item:
        :return:
        """

        fdItem = Feeds(**item)
        self.processDBentry(fdItem)
        return item
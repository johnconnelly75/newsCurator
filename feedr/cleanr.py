__author__ = 'john'


import pipelines
import simplejson as json
from models import FeedSources, Feeds
import feedparser
import time
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker


# newsFeed = pipelines.NewsFeedPipeline()
# session = newsFeed.Session()

# def getMaxID():
#     return session.query(func.max(FeedSources.id)).all()[0][0]


from models import FeedSources, Feeds, db_connect, create_tables



class cleanr(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        self.engine = db_connect()
        create_tables(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()


    def getFeeds(self):
        f1 = self.session.query(Feeds).all()
        return f1
        #f2 = session.query(Feeds).all()


    def deletr(self, id_):
        print '\t|Deleting', id_, '|'
        self.session.query(Feeds).filter_by(id=id_).delete()
        self.session.commit()
        print '\t\t|DELETED|'

    def matchr(self, r1):
        mrC = self.session.query(Feeds).filter_by(title=r1.title, summary=r1.summary).all()
        if len(mrC) > 1:
            return [x.id for x in mrC[1:]]

    def deDupe(self):
        f1 = self.getFeeds()
        deletions = 0
        print "Searching for matches to delete "
        for r1 in f1:
            ids = self.matchr(r1)
            if ids:
                print ids
                for id_ in ids:
                    deletions += 1
                    self.deletr(id_)

        print "Deleted {0} items...".format(deletions)

if __name__ == '__main__':
    while True:
        c = cleanr()
        c.deDupe()
        print '* *' * 50
        time.sleep(3600*2)

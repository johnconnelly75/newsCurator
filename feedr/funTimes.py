__author__ = 'john'
import pipelines
import simplejson as json
from models import FeedSources, Feeds
import feedparser
import time
from sqlalchemy.sql.expression import func
from cleanr import cleanr


newsFeed = pipelines.NewsFeedPipeline()
session = newsFeed.Session()

def getMaxID():
    return session.query(func.max(FeedSources.id)).all()[0][0]


def uploadExternalFeeds(feedr):
    nty = '/home/john/Documents/feedr/feedr/datas/nytFeedsSources.json'
    with open(feedr, 'rb') as fin:
        fR = fin.read()
        js = json.loads(fR)
        for j in js:
            print j
            j['id'] = getMaxID() + 1
            newsFeed.process_source(j)


def getFeeds():
    srcs = session.query(FeedSources).all()

    for src in srcs:
        row = [src.id, src.name_, src.url]
        print src.name_
        d = feedparser.parse(src.url)

        for ent in d['entries']:
            title = ent['title']
            summary = ent['summary'][:1550]
            link = ent['link']
            source = src.name_
            published = ent['published']
            rowCheck = session.query(Feeds).filter_by(title=title, summary=summary).first()
            #rowCheck = session.query(Feeds).filter_by(link=link).first()
            if rowCheck and (rowCheck.title == title and rowCheck.summary == summary):
                alreadyThere = True
            else:

                inputRow = {'title': title[:450], 'summary': summary[:1550], 'link': link[:550],
                            'source': source[:150], 'published': published, 'source_id': src.id}
                newsFeed.processFeedItem(inputRow)
                print '\t[UPLOADED]', title



if __name__ == '__main__':
    #uploadExternalFeeds(r'/home/john/Documents/feedr/feedr/datas/wsjFeedsSources.json')
    #uploadExternalFeeds(r'/home/john/Documents/feedr/feedr/datas/ftFeedsSources.json')

    while True:
        getFeeds()
        print '* *' * 50
        time.sleep(3600)

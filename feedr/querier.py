import pipelines
import simplejson as json
from models import FeedSources, Feeds
import feedparser
import time
from sqlalchemy.sql.expression import func
from cleanr import cleanr
import arrow


newsFeed = pipelines.NewsFeedPipeline()
session = newsFeed.Session()

srcs = session.query(Feeds).all()

for x in srcs:
    try:
        date = arrow.get(x.published, 'ddd, DD MMM YYYY HH:mm:ss Z')
    except arrow.parser.ParserError, e:
        try:
            date = arrow.get(x.published.replace('GMT', ''), 'ddd, DD MMM YYYY HH:mm:ss')
        except arrow.parser.ParserError, e:
            date = arrow.get(x.published)

    if date.format('DD-MM-YYYY') == arrow.now().format('DD-MM-YYYY'):
        print date.format('DD-MM-YYYY'), '| [{0}] -- '.format(x.source.encode('utf-8')), x.title

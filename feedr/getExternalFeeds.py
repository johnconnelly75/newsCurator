__author__ = 'john'



import requests
from lxml import html
import arrow
import simplejson as json


def getFeeds(url, src):
    #r = requests.get('http://www.nytimes.com/services/xml/rss/index.html')
    r = requests.get(url)
    print r.status_code


    rssFeeds = []
    body = html.fromstring(r.content)
    baddies = ['http://add.my.yahoo.com/rss?url=http://www.nytimes.com/services/xml/rss/yahoo/myyahoo/nyt_yahoo.xml']
    feedEndings = ['feed/', 'feed', 'xml', 'rss=1']
    ass = body.xpath('//a')
    for a in ass:
        href = a.get('href')
        if href and src == 'wsj':

            href = 'http://www.wsj.com' + href

        if href and href not in baddies:
            for en in feedEndings:
                if href.endswith(en):
                    row = {'name_': "{1}_{0}".format(a.text_content().strip().encode('utf-8'), src), 'url': href, 'dateAdded': arrow.now().format('MM/DD/YYYY')}
                    rssFeeds.append(row)

    js = json.dumps(rssFeeds)

    with open(r'/home/john/Documents/feedr/feedr/datas/{0}FeedsSources.json'.format(src), 'wb') as fout:
        fout.write(js)

def getWSJ_Feeds():
    wsj = 'http://www.wsj.com/public/page/rss_news_and_feeds.html'
    getFeeds(wsj, 'wsj')
#getWSJ_Feeds()

def getNYT_Feeds():
    nyt = 'http://www.nytimes.com/services/xml/rss/index.html'
    getFeeds(nyt, 'nyt')

def getFT_Feeds():
    src = 'ft'
    ft = 'http://www.ft.com/intl/rss'
    #getFeeds(ft, 'ft')
    r = requests.get(ft)
    print r.status_code
    rssFeeds = []
    body = html.fromstring(r.content)
    divvy = body.cssselect('div.linkList')

    for div in divvy:
        ass = div.xpath('ul/li/a')
        for a in ass:
            href = a.get('href')
            if href:
                row = {'name_': "{1}_{0}".format(a.text_content().strip().encode('utf-8'), src), 'url': href, 'dateAdded': arrow.now().format('MM/DD/YYYY')}
                print row
                rssFeeds.append(row)

    js = json.dumps(rssFeeds)
    with open(r'/home/john/Documents/feedr/feedr/datas/{0}FeedsSources.json'.format(src), 'wb') as fout:
        fout.write(js)

getFT_Feeds()

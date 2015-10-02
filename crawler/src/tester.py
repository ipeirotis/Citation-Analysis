__author__ = 'anna'




import urllib, urllib2, cookielib, traceback
#import requests # This command allows us to fetch URLs
from lxml import html # This module will allow us to parse the returned HTML/XML
#import pandas # To create a dataframe
import sys, datetime
import MySQLdb
import publicationCrawler


#Author Class Definition
class AuthorObject(object):
    def __init__(self, authorID, name):
        self.authorID = authorID
        self.name = name

def debug(*whatever):
    if not DEBUG: return
    for x in whatever:
        print >> sys.stderr, x,
    print >> sys.stderr

def authorC(authorID):
    # Let's start by fetching the page, and parsing it

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    url = "https://scholar.google.com/citations?hl=en&user=%s&view_op=list_works&sortby=pubdate&pagesize=100" % (authorID)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0')]
    opener.open(url)
    f = opener.open(url)
    doc = html.parse(f)

    # get author name
    authorNode = doc.find('.//div[@id="gsc_prf_in"]')
    authorName = authorNode.text_content()
    debug(authorName)


    #create author object
    authorObj = AuthorObject(authorID, authorName)


    return authorObj


DEBUG = False

if __name__ == "__main__":
    DEBUG = True
    #ask user :) !
    id = raw_input("Enter the author's Google Scholar ID you'd wish to spy on: ")
    #id = "sB4E4lcAAAAJ"
    #id = "jKvimFYAAAAJ"
    authObj = authorC(id)

import sys,urllib, urllib2, cookielib, traceback
#import requests # This command allows us to fetch URLs
from lxml import html # This module will allow us to parse the returned HTML/XML
#import pandas # To create a dataframe
import datetime
import MySQLdb



#Publication Class definition
class PublicationObject(object):
    def __init__(self, pubID, title, authors, publicationDate, totalCitations, citationGraph):
        self.pubID = pubID
        self.title = title
        self.authors = authors
        self.publicationDate = publicationDate
        self.totalCitations= totalCitations
        self.citationGraph = citationGraph


def create_PublicationObject(url):
    pubURL = url
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)    
    #opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36')]
    opener.open(pubURL)
    f = opener.open(pubURL)
    doc = html.parse(f)
    #print doc

    #headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    #headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0'}
    #response = requests.get(pubURL, headers=headers, verify = False)
    #doc = html.fromstring(response.text) # parse it and create a document
    #print (response)

    #get publication ID
    pubID = pubURL.split('citation_for_view=')[1]

    #get paper title
    #paperNode = doc.find('.//div[@id="gsc_ccl"]')
    titleNode = doc.find('.//*[@id="gsc_title"]')
    titleName = titleNode.text_content()
    #print(titleName)

    #paperInfoNode = doc.find('.//div[@id="gsc_table"]')
    #//*[@id="gsc_table"]/div[1]/div[2]
    #citationIndexes = citationsNodeTable.xpath('.//tr[0<position()<4]/td[2]//text()')


    #get paper authors
    '''
    authors = doc.xpath('.//*[@id="gsc_table"]/div[1]/div[2]//text()')
    print(authors[0])
    authorsList = authors[0].split(', ')
    print(authorsList)
    '''

    x = 0
    existAuth = False
    while doc.xpath('.//*[@id="gsc_table"]/div[%d]/div[1]//text()' % (x+1)):
        if doc.xpath('.//*[@id="gsc_table"]/div[%d]/div[1]//text()' % (x+1))[0] == 'Authors' or doc.xpath('.//*[@id="gsc_table"]/div[%d]/div[1]//text()' % (x+1))[0] == 'Inventors':
            x += 1
            existAuth = True
            break
        x += 1

    if existAuth:
        authors = doc.xpath('.//*[@id="gsc_table"]/div[%d]/div[2]//text()' % x)[0]
        #print(totalCitationsStr)
        authorsList = authors.split(', ')
        #print(authorsList)
    else:
        authorsList = 'none - report Google!'


    #get publication date
    '''
    publicationDateStr = (doc.xpath('.//*[@id="gsc_table"]/div[2]/div[2]//text()'))[0]
    print(publicationDateStr)
    pD = publicationDateStr.split('/')
    if len(pD) == 1:
        #publicationDate = datetime.date(int(pD[0]))
        #print(publicationDate.strftime("%Y"))
        publicationDate = datetime.date(int(pD[0]), 1, 1)
        print(publicationDate.strftime("%d/%m/%Y"))
    elif len(pD) == 2:
        #publicationDate = datetime.date(int(pD[0]), int(pD[1]))
        #print(publicationDate.strftime("%m/%Y"))
        publicationDate = datetime.date(int(pD[0]), int(pD[1]),1)
        print(publicationDate.strftime("%d/%m/%Y"))
    else:
        publicationDate = datetime.date(int(pD[0]), int(pD[1]), int(pD[2]))
        print(publicationDate.strftime("%d/%m/%Y"))
    '''

    x = 0
    existDate = False
    while doc.xpath('.//*[@id="gsc_table"]/div[%d]/div[1]//text()' % (x+1)):
        if doc.xpath('.//*[@id="gsc_table"]/div[%d]/div[1]//text()' % (x+1))[0] == 'Publication date':
            x += 1
            existDate = True
            break
        x += 1

    if existDate:
        publicationDateStr = (doc.xpath('.//*[@id="gsc_table"]/div[%d]/div[2]//text()' % x))[0]
        #print(publicationDateStr)
        pD = publicationDateStr.split('/')
        if len(pD) == 1:
            #publicationDate = datetime.date(int(pD[0]))
            #print(publicationDate.strftime("%Y"))
            publicationDate = datetime.date(int(pD[0]), 1, 1)
            #print(publicationDate.strftime("%d/%m/%Y"))
        elif len(pD) == 2:
            #publicationDate = datetime.date(int(pD[0]), int(pD[1]))
            #print(publicationDate.strftime("%m/%Y"))
            publicationDate = datetime.date(int(pD[0]), int(pD[1]),1)
            #print(publicationDate.strftime("%d/%m/%Y"))
        else:
            publicationDate = datetime.date(int(pD[0]), int(pD[1]), int(pD[2]))
            #print(publicationDate.strftime("%d/%m/%Y"))
    else:
        publicationDate = datetime.date(1900, 1, 1)
        #print(publicationDate.strftime("%d/%m/%Y"))




    #get total citations
    x = 0
    existCit = False
    while doc.xpath('.//*[@id="gsc_table"]/div[%d]/div[1]//text()' % (x+1)):
        if doc.xpath('.//*[@id="gsc_table"]/div[%d]/div[1]//text()' % (x+1))[0] == 'Total citations':
            x += 1
            existCit = True
            break
        x += 1

    if existCit:
        totalCitationsStr = doc.xpath('.//*[@id="gsc_table"]/div[%d]/div[2]/div[1]/a//text()' % x)[0]
        #print(totalCitationsStr)
        totalCitations = int(totalCitationsStr.split()[-1])
    else:
        totalCitations = 0

    #print("Total Citations are " + str(totalCitations))


    #get citations per year

    if doc.xpath('.//*[@id="gsc_graph_bars"]/span[1]//text()'):
        earliestYear = int(doc.xpath('.//*[@id="gsc_graph_bars"]/span[1]//text()')[0])
        a_style = doc.xpath('.//*[@id="gsc_graph_bars"]/a[1]')[0].get("style")
        z_index = int(a_style.split('z-index:')[1])
        latestYear = earliestYear + z_index - 1
        #print('latest year in citations chart is ' + str(latestYear))

    citationsGraph = []
    x = 1
    a = 1
    while doc.xpath('.//*[@id="gsc_graph_bars"]/span[%d]//text()' % x):
        cGYear = int(doc.xpath('.//*[@id="gsc_graph_bars"]/span[%d]//text()' % x)[0])
        #print(x)
        #print(cGYear)
        a_style = doc.xpath('.//*[@id="gsc_graph_bars"]/a[%d]' % a)[0].get("style")
        z_index = int(a_style.split('z-index:')[1])
        if (latestYear - z_index + 1) == cGYear:
            cGCitations = int(doc.xpath('.//*[@id="gsc_graph_bars"]/a[%d]/span//text()' % a)[0])
            a += 1
        else:
            cGCitations = 0
        citationsGraph.append((cGYear, cGCitations))
        x += 1

    #for x in citationsGraph:
         #print(x)

    pubObject = PublicationObject(pubID,titleName,authorsList,publicationDate,totalCitations,citationsGraph)
    return pubObject
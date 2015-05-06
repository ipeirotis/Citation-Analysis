__author__ = 'anna'


import requests # This command allows us to fetch URLs
from lxml import html # This module will allow us to parse the returned HTML/XML
import pandas # To create a dataframe
import sys, datetime
import publicationCrawler


#Author Class Definition
class AuthorObject(object):
    def __init__(self, authorID, name, totalCitations, H_index, coAuthors
        ,citationsPerYear, publications, publications_wo_date, lastTimeRetrieved):
        # PUBLICATIONS ARE STUB!! haven't clearly understood what we need out of it, apart from the urls.....
        # lastTimeRetrieved also a stub..
        self.authorID = authorID
        self.name = name
        self.totalCitations = totalCitations
        self.H_index = H_index
        self.coAuthors = coAuthors
        self.citationsPerYear = citationsPerYear
        self.publications = publications
        self.publications_wo_date = publications_wo_date
        self.lastTimeRetrieved = lastTimeRetrieved

def debug(*whatever):
    if not DEBUG: return
    for x in whatever:
        print >> sys.stderr, x,
    print >> sys.stderr

def authorCrawler(authorID, pubLimit=None):
    # Let's start by fetching the page, and parsing it
    url = "https://scholar.google.com/citations?hl=en&user=%s&view_op=list_works&sortby=pubdate&pagesize=100" % (authorID)
    headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0'}
    response = requests.get(url, headers=headers,
                            verify=False, allow_redirects=False)
    if response.is_redirect:
        print "Redirected to:"
        print response.headers['location']
        exit(1)
        
    # response = requests.get(url, verify="etc/ssl/certs/ca-certificates.crt") # get the html of that url
    doc = html.fromstring(response.text) # parse it and create a document
    debug(response)

    # get author name
    authorNode = doc.find('.//div[@id="gsc_prf_in"]')
    authorName = authorNode.text_content()
    debug(authorName)

    #check if authorObject exists in database
    #
    #
    #           TO DO!!
    #
    #

    # if exists, call updateAuthor function
    #
    #           TO DO (both check & function)
    #

    # if not exists

    # a. create authorObject
    #in case not ginven an authorID
    #authorHeadNode = doc.find('.//head')
    #debug(authorHeadNode)
    #authorIDHref = (authorHeadNode.find('.//link[@ref="canonical"]')).get("href")
    #debug(authorIDHref)

    #get total citations and h-index
    citationsNodeTable = doc.find('.//table[@id="gsc_rsb_st"]')
    #debug(citationsNodeTable)
    citationIndexes = citationsNodeTable.xpath('.//tr[0<position()<4]/td[2]//text()')

    totalCitations = citationIndexes[0]
    h_index = citationIndexes[1]
    debug(totalCitations)
    debug(h_index)

    #get co-authorsID's
    coAuthorsNode = doc.find('.//div[@id="gsc_rsb_co"]')
    debug(coAuthorsNode)
    #### OOOOPS!!! some author, i.e. Nikolaos Papaspyrou, don't gave a co-authors list
    #### also, no table... however, we could access https://scholar.google.com/citations?view_op=list_colleagues&hl=en&user=<USER_ID>
       # and from there parse the co-authors (gotta check also if the is a 'View More'/'Next' button

       ##### Take from "Publications" crawling..

    coAuthordIDs = []
    if doc.find('.//div[@id="gsc_rsb_co"]') is None:
        debug("No co-authors list exists")
    else :
        debug("Co-authors list exists")
        coAuthorsList = coAuthorsNode.find('.//ul[@class="gsc_rsb_a"]')
        coAuthors = coAuthorsList.findall(".//a")
        debug(coAuthors)
        urls = [lnk.get("href") for lnk in coAuthors]
        debug(urls)
        for url in urls:
            coAuthordIDs.append(url[16:len(url)-6])
        debug(coAuthordIDs)

    ##Do we also want the co-authors' names?

    # Get citations per year
    url_citations = "https://scholar.google.com/citations?hl=en&user=%s&view_op=citations_histogram" % (authorID)
    #headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0'}
    response = requests.get(url_citations, headers=headers, verify=False)
    doc_citations = html.fromstring(response.text)
    debug(response)
    #debug(doc_citations.text_content())
    #debug(doc_citations.xpath('.//*[@id="gsc_md_hist_b"]')[0])   #returns a div element
    doc_popup = doc_citations.xpath('.//*[@id="gsc_md_hist_b"]')[0]

    years = [int(x.text) for x in
             doc_popup.xpath('.//span[@class="gsc_g_t"]')]
    citationsPerYear = []
    for a in doc_popup.xpath('.//a[@class="gsc_g_a"]'):
        i = int(a.get("style").split('z-index:')[1])
        year = years[-i]
        citations = int(a.xpath('./span[@class="gsc_g_al"]')[0].text)
        citationsPerYear.append((year, citations))

    for x in citationsPerYear:
        debug(x)
                                
    #get publications
    x = 1
    publications = []
    publications_wo_date = []
    pubs_wo_date = 0
    '''
    while doc.xpath('.//*[@id="gsc_a_b"]/tr[%d]/td[1]/a' % (x)):
        pubUrl = 'https://scholar.google.com' + doc.xpath('.//*[@id="gsc_a_b"]/tr[%d]/td[1]/a' % (x))[0].get("href")
        #debug('pubUrl is ' + pubUrl)
        pubObject = publicationCrawler.create_PublicationObject(pubUrl)
        debug(pubObject.title)
        if pubObject.publicationDate.year == 1900:
            publications_wo_date.append(pubObject)
        else:
            publications.append(pubObject)
        x += 1
    '''

    while doc.xpath('.//*[@id="gsc_a_b"]/tr[%d]/td[1]/a' % (x)):
        pubUrl = 'https://scholar.google.com' + doc.xpath('.//*[@id="gsc_a_b"]/tr[%d]/td[1]/a' % (x))[0].get("href")
        #debug('pubUrl is ' + pubUrl)
        pubObject = publicationCrawler.create_PublicationObject(pubUrl)
        debug(pubObject.title)
        if pubObject.publicationDate.year == 1900:
            publications_wo_date.append(pubObject)
        else:
            publications.append(pubObject)
        x += 1
        if pubLimit is not None and x > pubLimit:
            break
    '''
    cstart = 0
    while not doc.xpath('.//button[@id="gsc_bpf_next"]')[0].get("disabled class"):
        cstart += 100
        url = "https://scholar.google.com/citations?hl=en&user=%s&view_op=list_works&sortby=pubdate&cstart=%d&pagesize=100"  % (authorID, cstart)
        headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        response = requests.get(url, headers=headers, verify = False)
        doc = html.fromstring(response.text) # parse it and create a document
        debug(response)
    '''
    #set lastTimeRetrieved
    lastTimeRetrieved = datetime.datetime.now()
    debug(lastTimeRetrieved)

    #create author object
    authorObj = AuthorObject(authorID, authorName, totalCitations, h_index, coAuthordIDs, citationsPerYear, publications, publications_wo_date, lastTimeRetrieved)
    return authorObj


DEBUG = False

if __name__ == "__main__":
    DEBUG = True
    #ask user :) !
    id = raw_input("Enter the author's Google Scholar ID you'd wish to spy on: ")
    #id = "sB4E4lcAAAAJ"
    #id = "jKvimFYAAAAJ"
    authObj = authorCrawler(id, 3)

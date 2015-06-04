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
    def __init__(self, authorID, name, totalCitations, H_index, i10_index, coAuthors
        ,citationsPerYear, publications, publications_wo_date, lastTimeRetrieved):
        # PUBLICATIONS ARE STUB!! haven't clearly understood what we need out of it, apart from the urls.....
        # lastTimeRetrieved also a stub..
        self.authorID = authorID
        self.name = name
        self.totalCitations = totalCitations
        self.H_index = H_index
        self.i10_index = i10_index
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
    
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)    
    url = "https://scholar.google.com/citations?hl=en&user=%s&view_op=list_works&sortby=pubdate&pagesize=100" % (authorID)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0')]
    opener.open(url)
    f = opener.open(url)
    doc = html.parse(f)
    #print doc
    #headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0'}
    #response = requests.get(url, headers=headers,
    #                        verify=False, allow_redirects=False)
    #if response.is_redirect:
        #print "Redirected to:"
        #print response.headers['location']
        #exit(1)
        
    #doc = html.fromstring(response.text) # parse it and create a document
    #debug(response)

    # Open database connection
    # db = MySQLdb.connect("localhost","root","gu1t@rri5ta")


    # Define your production Cloud SQL instance information.
    #_INSTANCE_NAME = 'citation-analysis:citation-analysis:sql'

    #open db connection for OCEAN
    #db = MySQLdb.connect("localhost","scholar","MjSwsqwtY5jjd3At")



    #open db connection for GAE
    #db = MySQLdb.connect(173.194.242.182,"programize","scholar123!")
    db = MySQLdb.connect(host='173.194.242.182', unix_socket='/cloudsql/citation-analysis:sql', user='programize2', passwd='scholar123!')




    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    cursor.execute("SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;")
    cursor.execute("SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;")
    cursor.execute("SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';")
    cursor.execute("CREATE SCHEMA IF NOT EXISTS scholar_db ;")
    db.commit()
    cursor.execute("USE scholar_db ;")
    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.authors ( \
           author_id VARCHAR(45) NOT NULL, \
           name VARCHAR(45) NULL, \
           total_citations INT NULL, \
           h_index INT NULL, \
           i10_index INT NULL, \
           last_time_retrieved DATETIME NULL, \
           PRIMARY KEY (author_id), \
           UNIQUE INDEX author_id_UNIQUE (author_id ASC)) \
           ENGINE = InnoDB; ")




    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.coauthors ( \
                    coauthor_id VARCHAR(45) NULL, \
                    authors_author_id VARCHAR(45) NOT NULL, \
                    PRIMARY KEY (coauthor_id, authors_author_id), \
                    CONSTRAINT fk_coauthors_authors1 \
                    FOREIGN KEY (authors_author_id) \
                    REFERENCES scholar_db.authors (author_id) \
                    ON DELETE NO ACTION \
                    ON UPDATE NO ACTION) \
                    ENGINE = InnoDB;")


    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.citations_per_year ( \
                    year INT NOT NULL, \
                    citations INT NULL, \
                    authors_author_id VARCHAR(45) NOT NULL,\
                    PRIMARY KEY (year, authors_author_id), \
                    INDEX fk_citations_per_year_authors1_idx (authors_author_id ASC), \
                    CONSTRAINT fk_citations_per_year_authors1 \
                    FOREIGN KEY (authors_author_id) \
                    REFERENCES scholar_db.authors (author_id) \
                    ON DELETE NO ACTION \
                    ON UPDATE NO ACTION) \
                    ENGINE = InnoDB;")



    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.publications ( \
                    publication_id VARCHAR(45) NOT NULL, \
                    title TEXT NULL, \
                    date DATE NULL, \
                    total_citations INT NULL, \
                    authors_author_id VARCHAR(45) NOT NULL, \
                    PRIMARY KEY (publication_id), \
                    INDEX fk_publications_authors1_idx (authors_author_id ASC), \
                    CONSTRAINT fk_publications_authors1 \
                    FOREIGN KEY (authors_author_id) \
                    REFERENCES scholar_db.authors (author_id) \
                    ON DELETE NO ACTION \
                    ON UPDATE NO ACTION) \
                    ENGINE = InnoDB;")



    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.pub_authors ( \
                    author_name VARCHAR(45) NULL, \
                    publications_publication_id VARCHAR(45) NOT NULL, \
                    PRIMARY KEY (author_name, publications_publication_id), \
                    INDEX fk_pub_authors_publications1_idx (publications_publication_id ASC), \
                    CONSTRAINT fk_pub_authors_publications1 \
                    FOREIGN KEY (publications_publication_id) \
                    REFERENCES scholar_db.publications (publication_id) \
                    ON DELETE NO ACTION \
                    ON UPDATE NO ACTION) \
                    ENGINE = InnoDB;")



    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.pub_citations_per_year ( \
                    year INT NOT NULL, \
                    citations INT NULL, \
                    publications_publication_id VARCHAR(45) NOT NULL, \
                    INDEX fk_pub_citations_per_year_publications1_idx (publications_publication_id ASC), \
                    CONSTRAINT fk_pub_citations_per_year_publications1 \
                    FOREIGN KEY (publications_publication_id) \
                    REFERENCES scholar_db.publications (publication_id) \
                    ON DELETE NO ACTION \
                    ON UPDATE NO ACTION) \
                    ENGINE = InnoDB;")


    cursor.execute("SET SQL_MODE=@OLD_SQL_MODE;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;")
    cursor.execute("SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;")

    db.commit()

    #db.close()


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

    #get total citations, h-index and i10-index
    citationsNodeTable = doc.find('.//table[@id="gsc_rsb_st"]')
    #debug(citationsNodeTable)
    citationIndexes = citationsNodeTable.xpath('.//tr[0<position()<4]/td[2]//text()')

    totalCitations = int(citationIndexes[0])
    h_index = int(citationIndexes[1])
    i10_index = int(citationsNodeTable.xpath('.//tr[4]/td[3]//text()')[0])  # i10 of the LAST 5 years
    debug(totalCitations)
    debug(h_index)
    debug(i10_index)

    #get co-authorsID's
    coAuthorsNode = doc.find('.//div[@id="gsc_rsb_co"]')
    debug(coAuthorsNode)

    coAuthorIDs = []
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
            coAuthorIDs.append(url[16:len(url)-6])
        debug(coAuthorIDs)

    ##Do we also want the co-authors' names?

    # Get citations per year
    url_citations = "https://scholar.google.com/citations?hl=en&user=%s&view_op=citations_histogram" % (authorID)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0')]
    opener.open(url_citations)
    f = opener.open(url_citations)
    doc_citations = html.parse(f)
    #print doc_citations

    #url_citations = "https://scholar.google.com/citations?hl=en&user=%s&view_op=citations_histogram" % (authorID)
    #headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    #headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0'}
    #response = requests.get(url_citations, headers=headers, verify=False)
    #doc_citations = html.fromstring(response.text)
    #debug(response)
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
        debug(pubObject.publicationDate.year)
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
    authorObj = AuthorObject(authorID, authorName, totalCitations, h_index, i10_index, coAuthorIDs, citationsPerYear, publications, publications_wo_date, lastTimeRetrieved)




    ##### TO-DO :
    # IF AUTHOR ALREADY EXISTS IN DATABASE, USE UPDATE!! (check in beginning..)

    # Prepare SQL query to INSERT a record into the database.
    sql = """INSERT INTO authors(author_id, name, total_citations, h_index, i10_index, last_time_retrieved) \
           VALUES ('%s', '%s', %d, %d, %d, '%s')""" % \
           (authorID, authorName, totalCitations, h_index, i10_index, lastTimeRetrieved.strftime('%Y-%m-%d %H:%M:%S'))

    try:
       cursor.execute(sql)
       db.commit()
    except:
       db.rollback()


    for co_ID in coAuthorIDs:
        sql = "insert into coauthors(coauthor_id, authors_author_id) select '%s', '%s' from authors limit 1;" % \
               (co_ID, authorID)

        try:
           cursor.execute(sql)
           db.commit()
        except:
            db.rollback()

    for citation in citationsPerYear:
        sql = "insert into citations_per_year(year, citations, authors_author_id) select %d, %d, '%s' from authors limit 1;" % \
               (citation[0], citation[1], authorID)

        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()


    for pub in publications:
        sql = "insert into publications(publication_id, title, date, total_citations, authors_author_id) \
               select '%s', '%s', '%s', %d, '%s' from authors limit 1;" % \
               (pub.pubID, pub.title, pub.publicationDate.strftime('%Y-%m-%d'), pub.totalCitations, authorID)

        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()

        for pub_auth in pub.authors:
            sql = "insert into pub_authors(author_name, publications_publication_id) \
                   select '%s', '%s' from publications limit 1;" % \
                   (pub_auth, pub.pubID)

            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()

        for pub_cit in pub.citationGraph:
            sql = "insert into pub_citations_per_year(year, citations, publications_publication_id) select %d, %d, '%s' from publications limit 1;" % \
                   (pub_cit[0], pub_cit[1], pub.pubID)

            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()

    # disconnect from server
    db.close()


    return authorObj


DEBUG = False

if __name__ == "__main__":
    DEBUG = True
    #ask user :) !
    id = raw_input("Enter the author's Google Scholar ID you'd wish to spy on: ")
    #id = "sB4E4lcAAAAJ"
    #id = "jKvimFYAAAAJ"
    authObj = authorCrawler(id, 3)

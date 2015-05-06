__author__ = 'anna'


import requests # This command allows us to fetch URLs
from lxml import html # This module will allow us to parse the returned HTML/XML
import pandas # To create a dataframe
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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


#ask user :) !
authorID = raw_input("Enter the author's Google Scholar ID you'd wish to spy on: ")


# Let's start by fetching the page, and parsing it
url = "https://scholar.google.com/citations?hl=en&user=%s&view_op=list_works&sortby=pubdate&pagesize=100"  % (authorID)
#headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0'}
response = requests.get(url, headers=headers, verify = False)
# response = requests.get(url, verify="etc/ssl/certs/ca-certificates.crt") # get the html of that url
doc = html.fromstring(response.text) # parse it and create a document
print (response)

#get author name
authorNode = doc.find('.//div[@id="gsc_prf_in"]')
authorName = authorNode.text_content()
print (authorName)

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
#print(authorHeadNode)
#authorIDHref = (authorHeadNode.find('.//link[@ref="canonical"]')).get("href")
#print(authorIDHref)


#get total citations and h-index
citationsNodeTable = doc.find('.//table[@id="gsc_rsb_st"]')
#print(citationsNodeTable)
citationIndexes = citationsNodeTable.xpath('.//tr[0<position()<4]/td[2]//text()')

totalCitations = citationIndexes[0]
h_index = citationIndexes[1]
print(totalCitations)
print(h_index)


#get co-authorsID's
coAuthorsNode = doc.find('.//div[@id="gsc_rsb_co"]')
print(coAuthorsNode)
#### OOOOPS!!! some author, i.e. Nikolaos Papaspyrou, don't gave a co-authors list
#### also, no table... however, we could access https://scholar.google.com/citations?view_op=list_colleagues&hl=en&user=<USER_ID>
   # and from there parse the co-authors (gotta check also if the is a 'View More'/'Next' button

   ##### Take from "Publications" crawling..

coAuthordIDs = []
if doc.find('.//div[@id="gsc_rsb_co"]') is None:
    print("No co-authors list exists")
else :
    print("Co-authors list exists")
    coAuthorsList = coAuthorsNode.find('.//ul[@class="gsc_rsb_a"]')
    coAuthors = coAuthorsList.findall(".//a")
    print(coAuthors)
    urls = [lnk.get("href") for lnk in coAuthors]
    print urls
    for url in urls:
        coAuthordIDs.append(url[16:len(url)-6])
    print(coAuthordIDs)

##Do we also want the co-authors' names?



#get citations per year
#//DIV[@id="gsc_md_hist_b"] exists NO MORE....
citationsPerYear = []
'''
citationsPerYearNode = doc.find('.//div[@id="gsc_md_hist_c"]')
print('citations per year:')
print(citationsPerYearNode)

cPYN = doc.xpath('//*[@id="gsc_md_hist_b"]')
print(cPYN)
'''

'''
driver = selenium.webdriver.Chrome()
#selenium.driver.get(url)
#citationsPerYearNode = selenium.driver.find_element_by_xpath('//div[@id="gsc_md_hist_b"]')
element = driver.find_element_by_id("gsc_g")
element.click()
citationsPerYearNode = driver.find_element_by_id("gsc_md_hist_b")
print(citationsPerYearNode)
'''

driver = webdriver.Firefox()
driver.implicitly_wait(1)
driver.get(url)
citationsPerYearNode = driver.find_element_by_id('gsc_g')
print(citationsPerYearNode)
#citationsPerYearNode.click()
driver.execute_script("document.getElementById('gsc_g').click()");
citationsPerYearPopUp = driver.find_element_by_id("gsc_md_hist_b")
print(citationsPerYearPopUp)
print(citationsPerYearPopUp.get_attribute('innerHTML'))

'''
        earliestYear = int(doc.xpath('.//*[@id="gsc_graph_bars"]/span[1]//text()')[0])
        a_style = doc.xpath('.//*[@id="gsc_graph_bars"]/a[1]')[0].get("style")
        z_index = int(a_style.split('z-index:')[1])
        latestYear = earliestYear + z_index - 1
        print('latest year in citations chart is ' + str(latestYear))
'''

doc_popup = html.fromstring(citationsPerYearPopUp.get_attribute('innerHTML'))
earliestYear = int(doc_popup.xpath('.//span[1]//text()')[0])
print('earliest pub in %d ' % earliestYear)
a_style = doc_popup.xpath('.//a[1]')[0].get("style")
z_index = int(a_style.split('z-index:')[1])
latestYear = earliestYear + z_index - 1
print('latest year in citations chart is ' + str(latestYear))


citationsPerYear = []
x = 1
a = 1
while doc_popup.xpath('.//span[%d]//text()' % x):
    cGYear = int(doc_popup.xpath('.//span[%d]//text()' % x)[0])
    #print(x)
    #print(cGYear)
    a_style = doc_popup.xpath('.//a[%d]' % a)[0].get("style")
    z_index = int(a_style.split('z-index:')[1])
    if (latestYear - z_index + 1) == cGYear:
        cGCitations = int(doc_popup.xpath('.//a[%d]/span//text()' % a)[0])
        a += 1
    else:
        cGCitations = 0
    citationsPerYear.append((cGYear, cGCitations))
    x += 1

for x in citationsPerYear:
    print(x)


#get publications
x = 1
publications = []
publications_wo_date = []
pubs_wo_date = 0
'''
while doc.xpath('.//*[@id="gsc_a_b"]/tr[%d]/td[1]/a' % (x)):
    pubUrl = 'https://scholar.google.com' + doc.xpath('.//*[@id="gsc_a_b"]/tr[%d]/td[1]/a' % (x))[0].get("href")
    #print('pubUrl is ' + pubUrl)
    pubObject = publicationCrawler.create_PublicationObject(pubUrl)
    print(pubObject.title)
    if pubObject.publicationDate.year == 1900:
        publications_wo_date.append(pubObject)
    else:
        publications.append(pubObject)
    x += 1
'''

while doc.xpath('.//*[@id="gsc_a_b"]/tr[%d]/td[1]/a' % (x)):
    pubUrl = 'https://scholar.google.com' + doc.xpath('.//*[@id="gsc_a_b"]/tr[%d]/td[1]/a' % (x))[0].get("href")
    #print('pubUrl is ' + pubUrl)
    pubObject = publicationCrawler.create_PublicationObject(pubUrl)
    print(pubObject.title)
    if pubObject.publicationDate.year == 1900:
        publications_wo_date.append(pubObject)
    else:
        publications.append(pubObject)
    x += 1
'''
cstart = 0
while not doc.xpath('.//button[@id="gsc_bpf_next"]')[0].get("disabled class"):
    cstart += 100
    url = "https://scholar.google.com/citations?hl=en&user=%s&view_op=list_works&sortby=pubdate&cstart=%d&pagesize=100"  % (authorID, cstart)
    headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    response = requests.get(url, headers=headers, verify = False)
    doc = html.fromstring(response.text) # parse it and create a document
    print (response)
'''
#set lastTimeRetrieved
lastTimeRetrieved = datetime.datetime.now()
print(lastTimeRetrieved)

#create author object
authorObj = AuthorObject(authorID, authorName, totalCitations, h_index, coAuthordIDs, citationsPerYear, publications, publications_wo_date, lastTimeRetrieved)

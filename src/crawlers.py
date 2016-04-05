import datetime
import time
from flask import request
from lxml import html
from urllib import urlencode
from urllib2 import build_opener, HTTPCookieProcessor, install_opener, Request
from cookielib import CookieJar

from main import app, db
from models import Author
from models import AuthorCitationsPerYear
from models import Publication
from models import PublicationCitationsPerYear

@app.route('/author/crawl', methods=['POST'])
def crawl_author():
  """
  Crawls Google Scholar in order to retrieve information about an author.
  """

  # The ID of the author in Google Scholar.
  scholar_id = request.form['scholar_id']

  print 'Crawl author ' + scholar_id

  # Retrieve the author with that ID (if any).
  author = Author.query.filter_by(scholar_id = scholar_id).first()
  if author is None:
    author = Author()

  cookie_jar = CookieJar()
  opener = build_opener(HTTPCookieProcessor(cookie_jar))
  install_opener(opener)

  url = 'https://scholar.google.com/citations';
  params = urlencode({'hl': 'en', 'view_op': 'list_works', 'sortby': 'pubdate',
                      'user': scholar_id, 'cstart': 1, 'pagesize': 2})
  req = Request(url + '?' + params)
  opener.open(req)
  res = opener.open(req)
  doc = html.parse(res)

  author.scholar_id = scholar_id

  nname = doc.find('.//div[@id="gsc_prf_in"]')
  if nname is not None:

    # The name of the author.
    author.name = nname.text_content()

  nemaildomain = doc.find('.//div[@id="gsc_prf_ivh"]')
  if nemaildomain is not None:

    # The domain where the author has an email.
    author.email_domain = nemaildomain.text_content().split(" - ")[0].split()[-1]

  ncitations = doc.find('.//table[@id="gsc_rsb_st"]')
  if ncitations is not None:

    # The total citations for the author.
    author.total_citations = ncitations.xpath('.//tr[2]/td')[1].text

    # The h-index for the author.
    author.h_index = ncitations.xpath('.//tr[3]/td')[1].text

    # The i10-index for the author.
    author.i10_index = ncitations.xpath('.//tr[4]/td')[1].text

  params = urlencode({'hl': 'en', 'view_op': 'citations_histogram',
                      'user': scholar_id})
  req = Request(url + '?' + params)
  opener.open(req)
  res = opener.open(req)
  doc = html.parse(res)

  # The citations per year for the author.
  author_citations_per_year = []
  nhistogram = doc.find('.//div[@id="gsc_md_hist_b"]')
  if nhistogram is not None:
    years = [x.text for x in nhistogram.xpath('.//span[@class="gsc_g_t"]')]
    for a in nhistogram.xpath('.//a[@class="gsc_g_a"]'):
      i = int(a.get("style").split('z-index:')[1])
      year = int(years[-i])
      citations_per_year = AuthorCitationsPerYear.query.filter_by(author_id = author.id, year = year).first()
      if citations_per_year is None:
        citations_per_year = AuthorCitationsPerYear()
      citations_per_year.year = int(years[-i])
      citations_per_year.citations = int(a.xpath('./span[@class="gsc_g_al"]')[0].text)
      author_citations_per_year.append(citations_per_year)
  author.citations_per_year = author_citations_per_year

  params = urlencode({'hl': 'en', 'view_op': 'list_colleagues', 'user': scholar_id})
  req = Request(url + '?' + params)
  opener.open(req)
  res = opener.open(req)
  doc = html.parse(res)

  # The co-authors of the author.
  author_coauthors = []
  for a in doc.xpath('.//h3[@class="gsc_1usr_name"]//a'):
    co_scholar_id = a.get('href').split('user=')[1].split('&hl')[0]
    coauthor = Author.query.filter_by(scholar_id = co_scholar_id).first()
    if coauthor is None:
      coauthor = Author()
    coauthor.scholar_id = co_scholar_id
    author_coauthors.append(coauthor)
  author.coauthors = author_coauthors

  # The publications.
  author_publications = []
  cstart = 1
  pagesize = 100
  while True:
    params = urlencode({'hl': 'en', 'view_op': 'list_works', 'sortby': 'pubdate',
                        'user': scholar_id, 'cstart': cstart, 'pagesize': pagesize})
    req = Request(url + '?' + params)
    opener.open(req)
    res = opener.open(req)
    doc = html.parse(res)

    for tr in doc.xpath('.//tr[@class="gsc_a_tr"]'):
      a = tr.find('.//td[@class="gsc_a_t"]//a')
      purl = a.get('href')

      # The ID of the publication in Google Scholar.
      pub_scholar_id = purl.split('citation_for_view=')[1]

      # Retrieve the publication with that ID (if any).
      publication = Publication.query.filter_by(scholar_id = pub_scholar_id).first()
      if publication is None:
        publication = Publication()
      publication.scholar_id = pub_scholar_id

      # The title of the publication.
      publication.title = a.text_content()

      pub_nyear = tr.find('.//td[@class="gsc_a_y"]//span')
      if pub_nyear is not None:
        year_of_publication = pub_nyear.text_content().strip()
        if year_of_publication:

          # The year of the publication.
          publication.year_of_publication = int(year_of_publication)

      pub_ncitations = tr.find('.//a[@class="gsc_a_ac"]')

      if pub_ncitations is not None:
        total_citations = pub_ncitations.text_content().strip()
        if total_citations:

          # The total citations for the publication.
          publication.total_citations = int(total_citations)

      author_publications.append(publication)

    if doc.xpath('.//button[@id="gsc_bpf_next"]')[0].get("disabled"):
      break

    cstart += 100
  author.publications = author_publications

  # When information about the author was retrieved from Google Scholar.
  author.retrieved_at = datetime.datetime.now()

  db.session.add(author)
  db.session.commit()

  print 'Crawled author ' + scholar_id + '.'
  return "Done."

@app.route('/publication/crawl', methods=['POST'])
def crawl_publication():
  """
  Crawls Google Scholar in order to retrieve information about a publication.
  """

  # The ID of the publication in Google Scholar.
  scholar_id = request.form['scholar_id']

  print 'Crawl publication ' + scholar_id

  url = 'https://scholar.google.com/citations';

  publication = Publication.query.filter_by(scholar_id = scholar_id).first()
  if publication is None:
    publication = Publication()

  cookie_jar = CookieJar()
  opener = build_opener(HTTPCookieProcessor(cookie_jar))
  install_opener(opener)

  url = 'https://scholar.google.com/citations';
  params = urlencode({'hl': 'en', 'view_op': 'view_citation', 'citation_for_view': scholar_id})
  req = Request(url + '?' + params)
  opener.open(req)
  res = opener.open(req)
  doc = html.parse(res)

  publication.scholar_id = scholar_id

  ntitle = doc.find('.//a[@class="gsc_title_link"]')
  if ntitle is not None:

    # The title of the publication.
    publication.title = ntitle.text_content()

  ntype = doc.find('.//div[@class="gs_scl"][3]//div[@class="gsc_field"]')
  if ntype is not None:

    # The type of the publication.
    publication.type = ntype.text_content()
    if publication.type == 'Description':
      publication.type = 'Other'

  nyear = doc.xpath('.//div[text()="Publication date"]/ancestor::div[@class="gs_scl"]//div[@class="gsc_value"]')
  if nyear is not None and len(nyear):

    # The year of the publication.
    publication.year_of_publication = int(nyear[0].text.split('/')[0])

  ncitations = doc.xpath('.//div[text()="Total citations"]/ancestor::div[@class="gs_scl"]//div[@class="gsc_value"]//a')
  if ncitations is not None and len(ncitations):

    # The total citations for the publication.
    publication.total_citations = ncitations[0].text.split(' ')[-1]

  nauthors = doc.xpath('.//div[text()="Authors"]/ancestor::div[@class="gs_scl"]//div[@class="gsc_value"]')
  if nauthors is not None and len(nauthors):

    # The authors of the publication.
    publication.author_names = nauthors[0].text

  # The citations per year for the publication.
  publication_citations_per_year = []
  nhistogram = doc.find('.//div[@id="gsc_graph_bars"]')
  if nhistogram is not None:
    years = [x.text for x in nhistogram.xpath('.//span[@class="gsc_g_t"]')]
    for a in nhistogram.xpath('.//a[@class="gsc_g_a"]'):
      i = int(a.get("style").split('z-index:')[1])
      year = int(years[-i])
      citations_per_year = PublicationCitationsPerYear.query.filter_by(publication_id = publication.id, year = year).first()
      if citations_per_year is None:
        citations_per_year = PublicationCitationsPerYear()
      citations_per_year.year = int(years[-i])
      citations_per_year.citations = int(a.xpath('./span[@class="gsc_g_al"]')[0].text)
      publication_citations_per_year.append(citations_per_year)
  publication.citations_per_year = publication_citations_per_year

  # When information about the author was retrieved from Google Scholar.
  publication.retrieved_at = datetime.datetime.now()

  db.session.add(publication)
  db.session.commit()

  print 'Crawled publication ' + scholar_id + '.'
  return "Done."

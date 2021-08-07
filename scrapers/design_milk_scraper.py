import requests
import json
import dateutil.relativedelta
import re
from tqdm import tqdm
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

from .utils import save_json, slugify, get_soup
from .utils import TODAY, SIX_MONTHS_AGO

DESIGN_MILK_HOME = 'https://design-milk.com'


# ==================================================================
# UTILS
# ==================================================================

def getPrevMonth(fromMonth=None, fromYear=None):
    month = datetime( fromYear, fromMonth, 1)
    prevMonth = month + dateutil.relativedelta.relativedelta(months=-1)
    return [ prevMonth.month, prevMonth.year ]


def getArchivePages(url):
     page_nums = range(20)
     return ["{}/page/{}".format(url, page_num) for page_num in page_nums]


def getArchiveLinksRecursive(_month, _year, _archive_links=[]):
    url = "{}/{}/{}".format(DESIGN_MILK_HOME, _year, _month)
    _date = datetime(_year, _month, 1)
    
    if _date < SIX_MONTHS_AGO:
        return _archive_links
    
    archive_pages = getArchivePages(url)
    _archive_links += archive_pages
    prevMonth, prevYear = getPrevMonth(_month, _year)
    return getArchiveLinksRecursive(prevMonth, prevYear, _archive_links)

# ==================================================================
# GET ARTICLE CARD INFO
# ==================================================================

def scrape_design_milk():
  archive_links = getArchiveLinksRecursive(TODAY.month, TODAY.year)

  articles = []
  for archive_link in tqdm(archive_links):
      html_archive_list = get_soup(archive_link)

      article_list_items = html_archive_list.findAll("div", attrs={"class": "article-list-item"})

      if len(article_list_items) == 0:
          continue

      for article_list_item in article_list_items:
          if article_list_item is not None and len(article_list_item.findChildren()) == 0:
              continue

          article_tag_a = article_list_item.find('a')
          article_href = article_tag_a['href']
          article_cover_image_src = (article_tag_a.find('img'))['src']

          article_title = article_list_item.find('h3')
          article_description = article_list_item.find('p')

          if article_title.text is not None:

            _article = {
              "id": slugify(article_title.text),
              "title": article_title.text,
              "href": article_href,
              "cover_image": article_cover_image_src,
              "description": article_description.text if article_description is not None else "",
            }

            articles.append(_article)

  for index, article in enumerate(articles, start=1):

    article_content = get_soup(article['href'])
    content_column = article_content.find("div", attrs={"class": "content-column"})
    details_div = article_content.find("div", attrs={"class": "details"})

    if content_column is None or details_div is None:
      continue

    article['date'] = details_div.find("div", attrs={"class": "date"}).text

    posted_by_link = details_div.find("a", attrs={"rel": "author"})
    article['posted_by_label'] = {
      "name": posted_by_link.text,
      "href": posted_by_link['href']
    }

    tags_div = details_div.find("div", attrs={"class": "tags"})
    article['tags'] = [ a.text for a in tags_div.findAll('a') ]
    article['body_raw'] = str(content_column)

  save_json('design-milk.json', articles)
import requests
import json
import uuid
import dateutil.relativedelta
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup

# ==================================================================
# UTILS
# ==================================================================

def saveJson(filename, data):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile)


def slugify(text):
  non_url_safe = ['"', '#', '$', '%', '&', '+',
                  ',', '/', ':', ';', '=', '?',
                  '@', '[', '\\', ']', '^', '`',
                  '{', '|', '}', '~', "'"]

  non_safe = [c for c in text if c in non_url_safe]
  if non_safe:
      for c in non_safe:
          text = text.replace(c, '')
          text = text.lower()
  # Strip leading, trailing and multiple whitespace, convert remaining whitespace to _
  text = u'-'.join(text.split())
  text = text.lower()
  return text


def getSoup(url):
    html_content = requests.get(url).text
    return BeautifulSoup(html_content, "lxml")


def getPrevMonth(fromMonth=None, fromYear=None):
    month = datetime( fromYear, fromMonth, 1)
    prevMonth = month + dateutil.relativedelta.relativedelta(months=-1)
    return [ prevMonth.month, prevMonth.year ]


def getArchivePages(url):
     page_nums = range(20)
     return ["{}/page/{}".format(url, page_num) for page_num in page_nums]


def getArchiveLinksRecursive(_month, _year, _archive_links=[]):
    url = "{}/{}/{}".format(DESIGN_MILK_HOME, _year, _month)

    if _year <= (TODAY.year - 2):
        return _archive_links
    
    archive_pages = getArchivePages(url)
    _archive_links += archive_pages
    prevMonth, prevYear = getPrevMonth(_month, _year)
    return getArchiveLinksRecursive(prevMonth, prevYear, _archive_links)

# ==================================================================
# CONSTANTS
# ==================================================================

DESIGN_MILK_HOME = 'https://design-milk.com'
TODAY = datetime.today()


# ==================================================================
# GET ARTICLE CARD INFO
# ==================================================================

archive_links = getArchiveLinksRecursive(TODAY.month, TODAY.year)

articles = []
for archive_link in tqdm(archive_links):
    html_archive_list = getSoup(archive_link)

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
            "parent_category_link": archive_link,
            "href": article_href,
            "cover_image": article_cover_image_src,
            "description": article_description.text if article_description is not None else "",
          }

          articles.append(_article)



# ==================================================================
# GET ARTICLE BODY INFO
# ==================================================================

for index, article in enumerate(articles, start=1):

  article_body = []
  article_content = getSoup(article['href'])

  # find article blocks
  content_column = article_content.find("div", attrs={"class": "content-column"})
  details_div = article_content.find("div", attrs={"class": "details"})

  if content_column is None or details_div is None:
    continue

  # parse details div
  article['date'] = details_div.find("div", attrs={"class": "date"}).text

  posted_by_link = details_div.find("a", attrs={"rel": "author"})
  article['posted_by_label'] = {
    "name": posted_by_link.text,
    "href": posted_by_link['href']
  }

  tags_div = details_div.find("div", attrs={"class": "tags"})
  article['tags'] = [ a.text for a in tags_div.findAll('a') ]
  article['body_raw'] = str(content_column)

  # parse content column
  for content_item in content_column.findAll('p'):

    item_image = content_item.find("img")
    if item_image is None:
      article_body.append({
        "type": "text",
        "value": content_item.text
      })
    else:
      try:
        article_body.append({
          "type": "image",
          "value": item_image['src'],
          "srcSet": item_image['srcset']
        })
      except:
        article_body.append({
          "type": "image",
          "value": item_image['src']
        })

  article['body'] = article_body

print('WRITING RESULT TO FILE')
saveJson('./public/data/articles.json', articles)
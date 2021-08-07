import json
import xmltodict
import requests
import re

from tqdm import tqdm
from datetime import datetime
from datetime import date
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from .utils import save_json, slugify, get_soup
from .utils import TODAY, SIX_MONTHS_AGO


# ==================================================================
# UTILS
# ==================================================================

def filter_by_date(item):
    year, month = (item['lastmod'][0:7]).split('-')
    item_date = datetime( int(year), int(month), 1)
    return item_date > SIX_MONTHS_AGO

def filter_by_loc(item):
    return "https://www.designboom.com/post-sitemap" in item['loc']

def get_xml(url):
    xml = requests.get(url)
    return xmltodict.parse(xml.text)

def scrape_design_boom():

    designboomxml = requests.get('https://www.designboom.com/sitemap_index.xml')
    data = xmltodict.parse(designboomxml.text)['sitemapindex']['sitemap']
    data = [ x for x in data if filter_by_date(x) ]
    data = [ x for x in data if filter_by_loc(x) ]

    article_cards = []
    print("GETTING ARTICLE INFORMATION")
    for item in tqdm(data):
        item_data = get_xml(item['loc'])['urlset']['url']
        item_data = [ x for x in item_data if filter_by_date(x) ]

        for link in item_data:

            _, __, ___, category, slug, ____ = link['loc'].split('/')
            match = re.search(r'\d{2}-\d{2}-\d{4}', link['loc'])

            if match is not None:
                try:
                    link_date = datetime.strptime(match.group(), '%m-%d-%Y')

                    if link_date > SIX_MONTHS_AGO:
                        _article = {
                            'href': link['loc'],
                            'date_timestamp': link_date.timestamp() * 1000,
                            'tags': [ category ]
                        }
                        article_cards = article_cards + [_article]
                    else:
                        continue
                except:
                    continue
            else:
                continue

    article_cards = sorted(article_cards, key=lambda k: k['date_timestamp'])

    data = []
    print("GETTING ARTICLE CONTENT")
    for article_item in tqdm(article_cards):
        try:
            article_page = get_soup( article_item['href'] )

            title_text = article_page.find("h1", attrs={"class": "post-title-inner"}).text
            article_item['title'] = title_text
            article_item['id'] = slugify(title_text)

            cover_image_wrapper = article_page.find("div", attrs={"class": "hero-sizer"})
            article_item['cover_image'] = cover_image_wrapper.find('img')['src']

            article_content = article_page.find("article", attrs={"class": "post-content"})
            article_item['description'] = ( article_content.find("p").text[0:125] + "..." ).capitalize()

            date_text = article_page.find("div", attrs={"class": "post-date"}).text
            article_item['date'] = parse(date_text).strftime("%m.%d.%Y")

            author_name = article_page.find("div", attrs={"class": "post-author"}).text
            article_item['posted_by_label'] = { "name": author_name, "href": None }

            article_item['body_raw'] = str(article_content)
            data.append(article_item)
        except:
            continue

    print("WRITING {} RESULTS".format(len(data)))
    save_json('design-boom.json', data)

if __name__ == 'main':
    print("MAIN")
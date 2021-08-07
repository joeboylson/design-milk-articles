import requests
import json
import dateutil.relativedelta
import re
import os

from tqdm import tqdm
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

STATIC_FOLDER_PATH = './static'
TODAY = datetime.today()
SIX_MONTHS_AGO = TODAY + relativedelta(months=-6)

def save_json(filename, data):
    static_filename = os.path.join(STATIC_FOLDER_PATH, filename)
    with open(static_filename, 'w') as outfile:
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

def get_soup(url):
    html_content = requests.get(url).text
    return BeautifulSoup(html_content, "lxml")

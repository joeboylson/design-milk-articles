import requests
import json
import uuid
import dateutil.relativedelta
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup

def getSoup(url):
    html_content = requests.get(url).text
    return BeautifulSoup(html_content, "lxml")

text = """
  <div class="content-column">

    This is some text

    <p>this is a paragraph</p>

    <img src="https://design-milk.com/images/2021/01/MENU_Eave_Dining_Sofa_Androgyne_Lounge_Table_Hashira_Table_Lamp-810x1080.jpg"/>

    <strong>Emphasized text</strong> 

    <a href="https://design-milk.com/images/2021/01/MENU_Eave_Dining_Sofa_Androgyne_Lounge_Table_Hashira_Table_Lamp-810x1080.jpg">
      this is a link
    </a>

  </div>
"""

# soup = BeautifulSoup(text, "lxml")
# div = soup.find('div')
# div_children = div.findAll(text=True)

# print( str(div) )
# print( div_children )

# soup = getSoup("https://design-milk.com/friday-five-with-ashley-rumsey-of-mason-studio/")
soup = BeautifulSoup(text, "lxml")
content = soup.find('div', attrs={'class': 'content-column'})

for child in content.findChildren(recursive=False):

  print(child)
  print(child.tag)
  print("")

  # if child.tag == 'div':
  #   image = child.find('img')
  #   print('IMAGE')
  #   print(image)
  #   continue
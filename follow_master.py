from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import html5lib
import threading
from urllib.request import urlopen

import pprint

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

list = {
    "Warren Buffett’s": "https://www.buffett.online/en/portfolio/",

}


df = pd.read_html("https://www.buffett.online/en/portfolio/")



# r = requests.get("https://www.buffett.online/en/portfolio/")
# # print(r.json())
# soup = BeautifulSoup(r.text, 'html.parser')
# print(soup.h2.text)
# tag = soup.find(class_="wp-block-table")
# for sub_tag in tag.find_all("td"):
#     print(sub_tag.text)
#
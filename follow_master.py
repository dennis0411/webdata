from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from lxml import etree, html

import pprint

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

list = {
    "Warren Buffett’s": "https://www.buffett.online/en/portfolio/",
    "BridgeWater": "https://whalewisdom.com/filer/bridgewater-associates-inc#tabholdings_tab_link",

}

df = pd.read_html("https://www.buffett.online/en/portfolio/")
new_df = pd.DataFrame(df[0])
data = new_df.iloc[1:-1].rename(columns=new_df.iloc[0])

# print(data)


url = "https://whalewisdom.com/filer/bridgewater-associates-inc#tabholdings_tab_link"
res = requests.get(url)
# 用lxml的html函式來處理內容格式
byte_data = res.content
source_code = html.fromstring(byte_data)
result = source_code.xpath('//*[@id="current_holdings_table"]/text()')
print(result)

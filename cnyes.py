from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import pprint

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

url = "https://news.cnyes.com"

sub_url = "/news/cat/us_stock"

target_url = url + sub_url

r = requests.get(target_url)

if r.status_code != requests.codes.ok:
    print("connect error : ", target_url)
else:
    print("getting data from : ", target_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    date = []
    time = []
    source = []
    title = []
    news = []
    market = []

    for tag in soup.find_all(class_="_67tN theme-meta"):
        datetime = tag.next_element['datetime']
        datetime_t = datetime.split('T')
        t = datetime_t[0]
        time.append(t)
        datetime_d = datetime_t[1].split('+')
        d = datetime_d[0]
        date.append(d)
        source.append('cnyes')
        market.append('us_stock')

    for tag in soup.find_all(class_="_1Zdp"):
        href = tag.get('href')
        link = url + href
        sub_r = requests.get(link)
        sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
        n = " "
        for sub_tag in sub_soup.h1:
            title.append(sub_tag.text)

        for sub_tag in sub_soup.find(class_="_1UuP"):
            for p in sub_tag.find_all('p'):
                a = p.text
                n = n + a
        news.append(n)

    news_data = pd.DataFrame(list(zip(date, time, source, market, title, news)),
                             columns=["date", "time", "source", "market", "title", "news"])
    print(news_data)

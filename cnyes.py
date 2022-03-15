from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import urllib.parse

import pprint

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

url = "https://news.cnyes.com"

news_url = {"us_stock": "/news/cat/us_stock",
            "world_stock": "/news/cat/wd_stock",
            "eu_asia_stock": "/news/cat/eu_asia_stock",
            "taiwan_stock": "/news/cat/tw_stock",
            "china_stock": "/news/cat/cn_stock",
            "crypto": "/news/cat/bc",
            "currency": "/news/cat/forex",
            "futures": "/news/cat/future",
            }

date = []
time = []
source = []
title = []
news = []
market = []

for sub_market in news_url.keys():
    target_url = url + news_url.get(sub_market)

    r = requests.get(target_url)

    if r.status_code != requests.codes.ok:
        print("connect error : ", target_url)
    else:
        print("getting data from : ", target_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        for tag in soup.find_all(class_="_1Zdp"):
            href = tag.get('href')
            link = url + href
            sub_r = requests.get(link)
            sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
            n = " "

            for sub_tag in sub_soup.find('time'):
                datetime = sub_tag.split(' ')
                t = datetime[0]
                time.append(t)
                d = datetime[1]
                date.append(d)
                source.append('cnyes')
                market.append(sub_market)

            for sub_tag in sub_soup.h1:
                title.append(sub_tag.text)

            for sub_tag in sub_soup.find(class_="_1UuP"):
                for p in sub_tag.find_all('p'):
                    a = p.text
                    n = n + a
            news.append(n)

# 中文例外
word_morningstar = "晨星專欄"
word_parse = urllib.parse.quote(word_morningstar)

target_url = url + f'/tag/{word_parse}'

r = requests.get(target_url)

if r.status_code != requests.codes.ok:
    print("connect error : ", target_url)
else:
    print("getting data from : ", target_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    for tag in soup.find_all(class_="_K_HZ"):
        href = tag.a.get('href')
        link = url + href
        sub_r = requests.get(link)
        sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
        n = " "

        for sub_tag in sub_soup.find('time'):
            datetime = sub_tag.split(' ')
            t = datetime[0]
            time.append(t)
            d = datetime[1]
            date.append(d)
            source.append('cnyes')
            market.append('morningstar')

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

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

cnyes_url = "https://news.cnyes.com"

cnyes_news_url = {"us_stock": "/news/cat/us_stock",
            "world_stock": "/news/cat/wd_stock",
            "eu_asia_stock": "/news/cat/eu_asia_stock",
            "taiwan_stock": "/news/cat/tw_stock",
            "china_stock": "/news/cat/cn_stock",
            "crypto": "/news/cat/bc",
            "currency": "/news/cat/forex",
            "futures": "/news/cat/future",
            }


# 物件化
class cnyes_source():
    def __init__(self):
        self.date = []
        self.time = []
        self.source = []
        self.title = []
        self.news = []
        self.market = []
        self.url = cnyes_url
        self.news_url = cnyes_news_url
        self.word_morningstar = "晨星專欄"

    def download_data(self):
        for sub_market in self.news_url.keys():
            target_url = self.url + self.news_url.get(sub_market)

            r = requests.get(target_url)

            if r.status_code != requests.codes.ok:
                print("connect error : ", target_url)
            else:
                print("getting data from : ", target_url)
                soup = BeautifulSoup(r.text, 'html.parser')

                for tag in soup.find_all(class_="_1Zdp"):
                    href = tag.get('href')
                    link = self.url + href
                    sub_r = requests.get(link)
                    sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
                    n = " "

                    for sub_tag in sub_soup.find('time'):
                        datetime = sub_tag.split(' ')
                        t = datetime[1]
                        self.time.append(t)
                        d = datetime[0]
                        self.date.append(d)
                        self.source.append('cnyes')
                        self.market.append(sub_market)

                    for sub_tag in sub_soup.h1:
                        self.title.append(sub_tag.text)

                    for sub_tag in sub_soup.find(class_="_1UuP"):
                        for p in sub_tag.find_all('p'):
                            a = p.text
                            n = n + a
                    self.news.append(n)

        # morningstar_report
        word_parse = urllib.parse.quote(self.word_morningstar)
        target_url = self.url + f'/tag/{word_parse}'
        r = requests.get(target_url)

        if r.status_code != requests.codes.ok:
            print("connect error : ", target_url)
        else:
            print("getting data from : ", target_url)
            soup = BeautifulSoup(r.text, 'html.parser')

            for tag in soup.find_all(class_="_K_HZ"):
                href = tag.a.get('href')
                link = self.url + href
                sub_r = requests.get(link)
                sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
                n = " "

                for sub_tag in sub_soup.find('time'):
                    datetime = sub_tag.split(' ')
                    t = datetime[1]
                    self.time.append(t)
                    d = datetime[0]
                    self.date.append(d)
                    self.source.append('cnyes')
                    self.market.append('morningstar')

                for sub_tag in sub_soup.h1:
                    self.title.append(sub_tag.text)

                for sub_tag in sub_soup.find(class_="_1UuP"):
                    for p in sub_tag.find_all('p'):
                        a = p.text
                        n = n + a
                self.news.append(n)

    def return_data(self):
        self.download_data()
        news_data = pd.DataFrame(list(zip(self.date, self.time, self.source, self.market, self.title, self.news)),
                                 columns=["date", "time", "source", "market", "title", "news"])
        return news_data


# N = cnyes_source()
# print(N.return_data())

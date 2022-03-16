from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import urllib.parse
import threading

import pprint

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)


# 物件化
class cnyes_source():
    def __init__(self):
        self.url = "https://news.cnyes.com"
        self.news_url = {"us_stock": "/news/cat/us_stock",
                         "world_stock": "/news/cat/wd_stock",
                         "eu_asia_stock": "/news/cat/eu_asia_stock",
                         "taiwan_stock": "/news/cat/tw_stock",
                         "china_stock": "/news/cat/cn_stock",
                         "crypto": "/news/cat/bc",
                         "currency": "/news/cat/forex",
                         "futures": "/news/cat/future",
                         }
        self.news_data = pd.DataFrame()

    def get_url_list(self):
        url_list = []
        market_list = []
        for submarket in self.news_url.keys():
            target_url = self.url + self.news_url.get(submarket)
            r = requests.get(target_url)
            soup = BeautifulSoup(r.text, 'html.parser')
            for tag in soup.find_all(class_="_1Zdp"):
                href = tag.get('href')
                link = self.url + href
                url_list.append(link)
                market_list.append(submarket)
        self.news_data = pd.DataFrame(columns=["date", "time", "source", "market", "title", "news", "link"],
                                      index=url_list)
        self.news_data["market"] = market_list

        return url_list

    def download_data(self, target_url):
        r = requests.get(target_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        news = " "
        tag = soup.find('time')
        datetime = tag.text.split(' ')
        t = datetime[1]
        d = datetime[0]
        source = 'cnyes'
        title = soup.h1.text

        for sub_tag in soup.find(class_="_1UuP"):
            for p in sub_tag.find_all('p'):
                a = p.text
                news += a

        self.news_data.loc[target_url, "time"] = t
        self.news_data.loc[target_url, "date"] = d
        self.news_data.loc[target_url, "source"] = source
        self.news_data.loc[target_url, "title"] = title
        self.news_data.loc[target_url, "news"] = news
        self.news_data.loc[target_url, "link"] = target_url

    def multi(self, url_list):
        threads = []
        for target_url in url_list:
            threads.append(threading.Thread(target=self.download_data, args=(target_url,)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def return_data(self):
        print(f'Loading data from cnyes')
        list = self.get_url_list()
        self.multi(list)

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import threading
import pprint

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

# 網址
tradingview_url = "https://tw.tradingview.com"

tradingview_news_url = {"us_stock": "/markets/stocks-usa/news/",
                        # "taiwan_stock": "/markets/stocks-taiwan/news/",
                        "china_stock": "/markets/stocks-china/news/",
                        "japan_stock": "/markets/stocks-japan/news/",
                        "currency": "/markets/currencies/news/",
                        "futures": "/markets/futures/news/",
                        "indices": "/markets/indices/news/",
                        "bonds": "/markets/bonds/news/",
                        "crypto": "/markets/cryptocurrencies/news/",
                        }


# 物件化
class tradingview_source():
    def __init__(self):
        self.date = []
        self.time = []
        self.source = []
        self.title = []
        self.news = []
        self.market = []
        self.url = tradingview_url
        self.news_url = tradingview_news_url

    def download_data(self, target_url, sub_market):
        r = requests.get(target_url)

        if r.status_code != requests.codes.ok:
            print("connect error : ", target_url)
        else:
            print("getting data from : ", target_url)
            soup = BeautifulSoup(r.text, 'html.parser')

            for tag in soup.find_all(class_="breadcrumbs-2r5p8wEW"):
                t = tag.span
                self.time.append(t.text)
                d = t.find_next()
                self.date.append(d.text)
                s = d.find_next()
                self.source.append(s.text)
                self.market.append(sub_market)
            for tag in soup.find_all(class_="title-2r5p8wEW"):
                self.title.append(tag.text)
            for tag in soup.find_all(class_="card-1NXd73hs cardLink-1NXd73hs"):
                href = tag.get('href')
                link = self.url + href
                sub_r = requests.get(link)
                sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
                for sub_tag in sub_soup.find(class_="body-2-Un7Upl body-1lnpJaR-"):
                    self.news.append(sub_tag.text)

    def multi(self):
        print("threads begin")
        threads = []
        for sub_market in self.news_url.keys():
            target_url = self.url + self.news_url.get(sub_market)
            threads.append(threading.Thread(target=self.download_data, args=(target_url, sub_market)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        print("threads end")

    def return_data(self):
        self.multi()
        news_data = pd.DataFrame(list(zip(self.date, self.time, self.source, self.market, self.title, self.news)),
                                 columns=["date", "time", "source", "market", "title", "news"])
        return news_data

# N = tradingview_source()
# print(N.return_data())

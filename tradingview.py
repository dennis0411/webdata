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

# 網址
news_dict = {"us_stock": "https://tw.tradingview.com/markets/stocks-usa/news/",
             "taiwan_stock": "https://tw.tradingview.com/markets/stocks-taiwan/news/",
             "china_stock": "https://tw.tradingview.com/markets/stocks-china/news/",
             "japan_stock": "https://tw.tradingview.com/markets/stocks-japan/news/",
             "currency": "https://tw.tradingview.com/markets/currencies/news/",
             "futures": "https://tw.tradingview.com/markets/futures/news/",
             "indices": "https://tw.tradingview.com/markets/indices/news/",
             "bonds": "https://tw.tradingview.com/markets/bonds/news/",
             "crypto": "https://tw.tradingview.com/markets/cryptocurrencies/news/",
             }

for country in news_dict.keys():
    url = news_dict.get(country)
    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        print("connect error : ", url)
    else:
        print("getting data from : ", url)
        soup = BeautifulSoup(r.text, 'html.parser')
        date = []
        time = []
        source = []
        title = []
        news = []
        market = []
        for tag in soup.find_all(class_="breadcrumbs-2r5p8wEW"):
            t = tag.span
            time.append(t.text)
            d = t.find_next()
            date.append(d.text)
            s = d.find_next()
            source.append(s.text)
            market.append(country)
        for tag in soup.find_all(class_="title-2r5p8wEW"):
            title.append(tag.text)
        for tag in soup.find_all(class_="card-1NXd73hs cardLink-1NXd73hs"):
            href = tag.get('href')
            link = "https://tw.tradingview.com" + href
            sub_r = requests.get(link)
            sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
            for sub_tag in sub_soup.find(class_="body-2-Un7Upl body-1lnpJaR-"):
                news.append(sub_tag.text)

        news_data = pd.DataFrame(list(zip(date, time, source, market, title, news)),
                                 columns=["date", "time", "source", "market", "title", "news"])
        print(news_data)

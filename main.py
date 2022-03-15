import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import tradingview
import cnyes
import time

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




if __name__ == '__main__':
    t = tradingview.tradingview_source()
    df1 = t.return_data()
    c = cnyes.cnyes_source()
    df2 = c.return_data()
    data = pd.concat([df1, df2], ignore_index=True)
    print(data)

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

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "cookie": "_gcl_au=1.1.1435175802.1647566308; _gid=GA1.2.895656006.1647566308; _hjSessionUser_2568576=eyJpZCI6ImEyNmQ2Y2NmLTI1ODQtNTA5OS05NjNjLWVlMzI1MzQwZGYwMiIsImNyZWF0ZWQiOjE2NDc1NjYzMDg4NTksImV4aXN0aW5nIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; _hjSession_2568576=eyJpZCI6IjVjNjgwN2U4LTE2ZGItNGZmMy1hYzMyLWZhNjYzMDAzYjA5MCIsImNyZWF0ZWQiOjE2NDc1ODYwMzQ1NDUsImluU2FtcGxlIjp0cnVlfQ==; finboxio-production:refresh=b9dd07fe-42fd-4295-a876-897d9577a0cd; finboxio-production:refresh.sig=XHZ2YwCyC__gh5degH02zYwoOsI; _ga=GA1.2.924174480.1647566308; finboxio-production:jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MjQ5NCwidmlzaXRvcl9pZCI6InYtNzQ5cmxpZTgzeDkiLCJmaXJzdF9zZWVuIjoiMjAyMC0xMC0xOVQxMzoxMjo0OC4xNDdaIiwicHJldmlld19hY2Nlc3MiOnsiYXNzZXRzX3ZpZXdlZCI6W10sImFzc2V0c19tYXgiOjV9LCJyb2xlcyI6WyJ1c2VyIiwiYmxvY2tlZCJdLCJib29zdHMiOltdLCJyZWdpb25zIjpbXSwic2NvcGVzIjpbInJvbGU6dXNlciIsInJvbGU6YmxvY2tlZCJdLCJleHAiOjE2NDc1OTA5NTYsImlhdCI6MTY0NzU5MDY1N30.DiBHHpYz6LABUwELYwfodIL5NtPIXx43zKoE-L9aHvE; finboxio-production:jwt.sig=k3j6qHLefxi3d0Jmmy6S0vGOUEE; smplog-trace=4kn3Bnqq6CB-MiOH0_GxJ4E_OqGemTD2xZGmveJkKCkYSefCN2v8Dg==; _ga_SE2BNZKPPC=GS1.1.1647588401.3.1.1647590684.0; _dd_s=logs=1&id=d50c7230-d5ef-4896-a01f-f1a4c131b69e&created=1647588399152&expire=1647592010674",
}

url = "https://finbox.com/ideas/warren-buffett"
r = requests.get(url)
# print(r.json())
soup = BeautifulSoup(r.text, 'html.parser')
tag = soup.find(class_='rt-tbody')
print(tag.text)


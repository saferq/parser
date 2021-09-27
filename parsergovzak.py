from pprint import pprint

import feedparser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# url = 'https://zakupki.gov.ru/epz/order/extendedsearch/rss.html?searchString=демонтаж&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=true&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&currencyIdGeneral=-1&customerPlace=5277377%2C5277362&customerPlaceCodes=OKER34%2COKER33&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'

# feeds = feedparser.parse(url).entries

# for feed in feeds:
#     print('--------')
#     print(feed['author'])
#     parse_url = feed['link']
#     print(parse_url)
#     # res = requests.get(parse_url, headers={"User-Agent": "Mozilla/5.0"})
#     # soup = BeautifulSoup(res.text, "lxml")
#     res = requests.get(parse_url)
#     soup = BeautifulSoup(res, "lxml")
#     # n1 = soup.find_all('td')
#     print(soup.prettify())

parse_url = 'https://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?regNumber=31501961460'
print(parse_url)
# res = requests.get(parse_url, headers={"User-Agent": "Mozilla/5.0"})
# # res = requests.get(parse_url)
# soup = BeautifulSoup(res.text, "lxml")

browser = webdriver.Chrome()
browser.get(parse_url)
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
# n1 = soup.find_all('td')
print(soup)

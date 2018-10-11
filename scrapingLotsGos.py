import urllib2
import time
from django.utils.encoding import smart_str
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
from tabulate import tabulate
import os
import json

link_page = 'http://zakupki.gov.kg/popp/view/order/view.xhtml?id='

lots = []
# data_ri = []
page = link_page + '128014811'

driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(page)
button = driver.find_element_by_link_text('RU')
button.click()

soup = BeautifulSoup(driver.page_source, 'html.parser')
# soup = BeautifulSoup(driver.page_source, 'html.parser')

for body in soup.findAll('body'):
    content = body.find('span', {'class': 'field-groups-view m-left m-right'})
    for div in content.findAll('tbody', {'class': 'ui-datatable-data ui-widget-content'}):
        last_tr = div.find_all('tr')[-1]
        if 'data-ri' in last_tr.attrs:
            tr_num = last_tr["data-ri"]
last_num = int(tr_num)
# print last_num
d = last_num * 2 + 1

x = 1
b = str(d)
time.sleep(6)

while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for body in soup.findAll('body'):
        content = body.find('span', {'class': 'field-groups-view m-left m-right'})
        for div in content.findAll('tbody', {'class': 'ui-datatable-data'}):
            resultText = div.prettify()
            for row in BeautifulSoup(resultText)('tr', {'class': 'ui-expanded-row-content ui-widget-content childRowFillBG'}):
                lots.append([row.text])

    a = str(x)
    time.sleep(6)
    xpath = '//tbody[@id="j_idt69:lotsTable_data"]/tr[' + a + ']/td[8]/div'
    button = driver.find_element_by_xpath(xpath)
    button.click()
    x += 2
    if a == b:
        break

jsonD = json.dumps(lots)

print jsonD.decode('unicode_escape')
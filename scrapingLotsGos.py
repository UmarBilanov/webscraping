# -*- coding: utf-8 -*-
import urllib2
import pymongo

from django.utils.encoding import smart_str
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import os
import json
import time

# list_page = 'http://zakupki.gov.kg/popp/view/order/list.xhtml'

link_page = 'http://zakupki.gov.kg/popp/view/order/view.xhtml?id='

def get_lots_info():
    page = link_page + '130452757'
    lots = []
    resultText = []
    resultLabel = []

    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(page)
    button = driver.find_element_by_link_text('RU')
    button.click()

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('span', {'class': 'field-groups-view m-left m-right'})
        for div in content.findAll('tbody', {'class': 'ui-datatable-data ui-widget-content'}):
            last_tr = div.find_all('tr')[-1]
            if 'data-ri' in last_tr.attrs:
                tr_num = last_tr["data-ri"]
    last_num = int(tr_num)
    d = last_num * 2 + 1

    x = 1
    b = str(d)
    time.sleep(5)

    while True:
        a = str(x)
        time.sleep(6)
        xpath = '//tbody[@id="j_idt69:lotsTable_data"]/tr[' + a + ']/td[8]/div'
        button = driver.find_element_by_xpath(xpath)
        button.click()
        x += 2

        if a == b:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for body in soup.findAll('body'):
        content = body.find('span', {'class': 'field-groups-view m-left m-right'})
        for div in content.findAll('tbody', {'class': 'ui-datatable-data'}):
            for row in div('tr'):
                for cell in row('td'):
                    for span in cell.findAll('span', {'class': 'bold'}):
                        lots.append(span.text)

            for row in div.findAll('tr', {'class': 'ui-expanded-row-content ui-widget-content childRowFillBG'}):
                for table in row.findAll('table', {'class': 'display-table private-room-table no-borders f-right'}):
                    for th in table('th'):
                        resultLabel.append(smart_str(th.text))
                    for td in table('td'):
                        resultText.append(smart_str(td.text))

    list_of_lists = [lots[i:i + 5] for i in range(0, len(lots), 5)]
    # jsonD = json.dumps(lots)
    lotsSpecifies = [{l: t} for l, t in zip(resultLabel, resultText)]
    # gen_info =
    jsonD = json.dumps(list_of_lists)

    print jsonD.decode('unicode_escape')

    driver.close()



# def geting_lots_info():
#     resultLabel = ['№', 'Наименование лота', 'Сумма', 'Адрес и Место поставки', 'Сроки поставки товара ']
#     resultText = []
#     gen_info = {}
#     page = urllib2.urlopen(link_page + '130452757')
#
#     soup = BeautifulSoup(page, 'html.parser')
#     # soup = BeautifulSoup(driver.page_source, 'html.parser')
#
#     for body in soup.findAll('body'):
#         content = body.find('span', {'class': 'field-groups-view m-left m-right'})
#         for div in content.findAll('tbody', {'class': 'ui-datatable-data'}):
#             for row in div('tr'):
#                 for cell in row('td'):
#                     for span in cell.findAll('span', {'class': 'bold'}):
#                         resultText.append(span.text)
#
#     list_of_lists = [resultText[i:i + 5] for i in range(0, len(resultText), 5)]
#     # jsonT = json.dumps(list_of_lists)
#     # print jsonT.decode('unicode_escape')
#
#     list_of_lists.append(resultLabel)
#     # jsonL = json.dumps(list_of_lists)
#     # print jsonL.decode('unicode_escape')
#     l = len(list_of_lists)
#     gen_info = {z[l-1]: list(z[0:l-2]) for z in zip(*list_of_lists)}
#
#     # gen_info = [{z[0]: list(z[1:])} for z in zip(resultLabel, list_of_texts)]
#     jsonD = json.dumps(gen_info)
#     return jsonD.decode('unicode_escape')
#
# def get_extralots_info():
#     # lots = []
#     resultLabel = []
#     resultText = []
#     # data_ri = []
#     page = link_page + '128014811'
#
#     driver = webdriver.Firefox()
#     driver.implicitly_wait(30)
#     driver.get(page)
#     button = driver.find_element_by_link_text('RU')
#     button.click()
#
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     # soup = BeautifulSoup(driver.page_source, 'html.parser')
#
#     for body in soup.findAll('body'):
#         content = body.find('span', {'class': 'field-groups-view m-left m-right'})
#         for div in content.findAll('tbody', {'class': 'ui-datatable-data ui-widget-content'}):
#             last_tr = div.find_all('tr')[-1]
#             if 'data-ri' in last_tr.attrs:
#                 tr_num = last_tr["data-ri"]
#     last_num = int(tr_num)
#     # print last_num
#     d = last_num * 2 + 1
#
#     x = 1
#     b = str(d)
#     time.sleep(5)
#
#     while True:
#         a = str(x)
#         time.sleep(6)
#         xpath = '//tbody[@id="j_idt69:lotsTable_data"]/tr[' + a + ']/td[8]/div'
#         button = driver.find_element_by_xpath(xpath)
#         button.click()
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         x += 2
#         for body in soup.findAll('body'):
#             content = body.find('span', {'class': 'field-groups-view m-left m-right'})
#             for div in content.findAll('tbody', {'class': 'ui-datatable-data'}):
#                 for row in div.findAll('tr', {'class': 'ui-expanded-row-content ui-widget-content childRowFillBG'}):
#                     for table in row.findAll('table', {'class': 'display-table private-room-table no-borders f-right'}):
#                         for th in table('th'):
#                             resultLabel.append(smart_str(th.text))
#                         for td in table('td'):
#                             resultText.append(smart_str(td.text))
#         if a == b:
#             break
#
#     gen_info = [{l: t} for l, t in zip(resultLabel, resultText)]
#     jsonD = json.dumps(gen_info)
#
#     return jsonD.decode('unicode_escape')


get_lots_info()
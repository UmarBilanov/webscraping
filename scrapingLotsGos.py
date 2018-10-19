# -*- coding: utf-8 -*-
import json
import urllib2

import xmltodict
from bs4 import BeautifulSoup
from django.utils.encoding import smart_str
from selenium import webdriver
import time

link_page = 'http://zakupki.gov.kg/popp/view/order/view.xhtml?id='


def get_lots_info():
    resultLabel = ['№', 'Наименование лота', 'Сумма', 'Адрес и Место поставки', 'Сроки поставки товара ']
    resultText = []
    gen_info = {}
    page = urllib2.urlopen(link_page + '126401206')

    soup = BeautifulSoup(page, 'html.parser')
    # soup = BeautifulSoup(driver.page_source, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('span', {'class': 'field-groups-view m-left m-right'})
        for div in content.findAll('tbody', {'class': 'ui-datatable-data'}):
            for row in div('tr'):
                for cell in row('td'):
                    for span in cell.findAll('span', {'class': 'bold'}):
                        resultText.append(span.text)

    list_of_lists = [resultText[i:i + 5] for i in range(0, len(resultText), 5)]
    # jsonT = json.dumps(list_of_lists)
    # print jsonT.decode('unicode_escape')

    list_of_lists.append(resultLabel)
    # jsonL = json.dumps(list_of_lists)
    # print jsonL.decode('unicode_escape')
    l = len(list_of_lists)
    gen_info = {z[l - 1]: list(z[0:l - 2]) for z in zip(*list_of_lists)}

    # gen_info = [{z[0]: list(z[1:])} for z in zip(resultLabel, list_of_texts)]
    jsonD = json.dumps(gen_info)
    print jsonD.decode('unicode_escape')


def get_pay_info():
    resultText = []
    page = urllib2.urlopen(link_page + '126401206')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        for div in body.findAll('div', {'class': 'row no-gutters'}):
            for tbody in div.findAll('tbody'):
                for cell in tbody('td'):
                    resultText.append(smart_str(cell.text))

    l = resultText[0::2]
    t = resultText[1::2]

    gen_info = [{l: t} for l, t in zip(l, t)]
    jsonD = json.dumps(gen_info)
    print jsonD.decode('unicode_escape')


def get_requirements():
    resultLabel = ['Квалификация', 'Требование']
    resultText = []
    page = urllib2.urlopen(link_page + '126401206')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        div = body.find('table', {'class': 'publicTableData'})
        for tbody in div.findAll('tbody'):
            for cell in tbody('td'):
                resultText.append(smart_str(cell.text))

    list_of_lists = []
    resultClass = resultText[1::3]
    resultReq = resultText[2::3]
    list_of_lists.append(resultClass)
    list_of_lists.append(resultReq)
    # list_of_lists.append(resultLabel)

    # l = len(list_of_lists)
    # gen_info = {z[l - 1]: list(z[0:l - 2]) for z in zip(*list_of_lists)}
    #
    gen_info = [{z[0]: z[1:]} for z in zip(resultLabel, list_of_lists)]
    jsonD = json.dumps(gen_info)
    print jsonD.decode('unicode_escape')

    # for div in body.findNextSiblings('table', {'class': 'publicTableData'}):


def get_criteria():
    resultText = []
    page = urllib2.urlopen(link_page + '126401206')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        div = body.find('table', {'class': 'publicTableData equal'})
        for tbody in div.findAll('tbody'):
            for cell in tbody('td'):
                resultText.append(smart_str(cell.text))

    # jsonD = json.dumps(resultText)
    # print jsonD.decode('unicode_escape')

    l = resultText[0::2]
    t = resultText[1::2]

    gen_info = [{l: t} for l, t in zip(l, t)]
    jsonD = json.dumps(gen_info)
    print jsonD.decode('unicode_escape')


def get_extralots_info():
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
    time.sleep(5)

    while True:
        a = str(x)
        time.sleep(6)
        xpath = '//tbody[@id="j_idt69:lotsTable_data"]/tr[' + a + ']/td[8]/div'
        button = driver.find_element_by_xpath(xpath)
        button.click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        x += 2
        for body in soup.findAll('body'):
            content = body.find('span', {'class': 'field-groups-view m-left m-right'})
            for div in content.findAll('tbody', {'class': 'ui-datatable-data'}):
                for row in div.findAll('tr', {'class': 'ui-expanded-row-content ui-widget-content childRowFillBG'}):
                    for table in row.findAll('table', {'class': 'display-table private-room-table no-borders f-right'}):
                        lots.append([table.text])
        if a == b:
            break

    jsonD = json.dumps(lots)
    return jsonD.decode('unicode_escape')

# get_lots_info()
# get_pay_info()
# get_requirements()
get_criteria()
print get_extralots_info()

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
#
# mylist = []
# mylist = jsonD.decode('unicode_escape')
#
# x = mycol.insert_many(mylist)

# print(x)

# -*- coding: utf-8 -*-
import json
import urllib2

import xmltodict
from bs4 import BeautifulSoup
from django.utils.encoding import smart_str
from selenium import webdriver

link_page = 'http://zakupki.gov.kg/popp/view/order/view.xhtml?id='


def get_gen_info():
    data = {}
    page = link_page + '128014811'
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(page)
    button = driver.find_element_by_link_text('RU')
    button.click()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for body in soup.findAll('body'):
        content = body.find('div', {'class': 'container-content'})
        for col in content.findAll('div', {'class': 'row'}):
            data = col.prettify()

    jsonD = json.dumps(xmltodict.parse(data))
    genInfo = jsonD.decode('unicode_escape')

    print genInfo
    # return jsonD.decode('unicode_escape')


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
    gen_info = {z[l-1]: list(z[0:l-2]) for z in zip(*list_of_lists)}

    # gen_info = [{z[0]: list(z[1:])} for z in zip(resultLabel, list_of_texts)]
    jsonD = json.dumps(gen_info)
    print jsonD.decode('unicode_escape')


# get_gen_info()
get_lots_info()
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
#
# mylist = []
# mylist = jsonD.decode('unicode_escape')
#
# x = mycol.insert_many(mylist)

# print(x)

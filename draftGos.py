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


# def get_data_rk():
#     data_rk = []
#     # page = urllib2.urlopen(list_page)
#     url = "http://zakupki.gov.kg/popp/home.xhtml"
#
#     # create a new Firefox session
#     driver = webdriver.Firefox()
#     driver.implicitly_wait(30)
#     driver.get(url)
#     button = driver.find_element_by_link_text('Advanced search')
#     button.click()
#     button = driver.find_element_by_xpath('//div[@id="tv1:status"]/ul')
#     button.click()
#     button = driver.find_element_by_xpath('//div[@id="tv1:status_panel"]/div[2]/ul/li/div/div[2]/span')
#     button.click()
#     button = driver.find_element_by_xpath('//div[@id="tv1:status_panel"]/div/a')
#     button.click()
#     button = driver.find_element_by_xpath('//div[@id="tv1:ate"]/ul')
#     button.click()
#     button = driver.find_element_by_xpath('//div[@id="tv1:ate_panel"]/div[2]/ul/li[6]/div/div[2]/span')
#     button.click()
#     button = driver.find_element_by_xpath('//div[@id="tv1:ate_panel"]/div/a')
#     button.click()
#     button = driver.find_element_by_xpath('//input[@name=\'tv1:j_idt152\']')
#     button.click()
#
#
#     while True:
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         for tr in soup.findAll('tr', {'class': 'ui-widget-content'}):
#             if 'data-rk' in tr.attrs:
#                 data_rk.append(tr["data-rk"])
#         time.sleep(6)
#         button = driver.find_element_by_xpath('//div[@id=\'j_idt104:j_idt105:table_paginator_bottom\']/a[3]')
#         button.click()
#         # print data_rk
#         if 'ui-state-disabled' in button.get_attribute('class'):
#             break
#     # print data_rk
#     return data_rk

# print (get_data_rk())

def get_general_info():
    resultLabel = []
    resultText = []
    # jsonD = []
    page = urllib2.urlopen(link_page + '130452757')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('div', {'class': 'container-content'})
        # col = content.find('div', {'class': 'row'})
        for div in content.findAll('div', {'class': 'col-12 col-md-6'}):
            for span in div.findAll('span', {'class': 'label'}):
                resultLabel.append(smart_str(span.text))
            for span1 in div.findAll('span', {'class': 'text'}):
                resultText.append(smart_str(span1.text))
        gen_info = {l: t for l, t in zip(resultLabel, resultText)}
        jsonD = json.dumps(gen_info)

    return jsonD.decode('unicode_escape')

def get_organization_info():
    resultLabel = []
    resultText = []
    # jsonD = []
    page = urllib2.urlopen(link_page + '130452757')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('div', {'class': 'container-content'}).findNextSibling('div',
                                                                                   {'class': 'container-content'})
        # col = content.find('div', {'class': 'row'}).next_sibling('div', {'class': 'row'})
        for div in content.findAll('div', {'class': 'col-12 col-md-6'}):
            for span in div.findAll('span', {'class': 'label'}):
                resultLabel.append(smart_str(span.text))
            for span1 in div.findAll('span', {'class': 'text'}):
                resultText.append(smart_str(span1.text))
        gen_info = {l: t for l, t in zip(resultLabel, resultText)}
        jsonD = json.dumps(gen_info)

    return jsonD.decode('unicode_escape')

def get_lots_info():
    resultLabel = ['№', 'Наименование лота', 'Сумма', 'Адрес и Место поставки', 'Сроки поставки товара ']
    resultText = []
    gen_info = {}
    page = urllib2.urlopen(link_page + '130452757')

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
    return jsonD.decode('unicode_escape')

def get_extralots_info():
    # lots = []
    resultLabel = []
    resultText = []
    # data_ri = []
    page = link_page + '130452757'

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
                        for th in table('th'):
                            resultLabel.append(smart_str(th.text))
                        for td in table('td'):
                            resultText.append(smart_str(td.text))
        if a == b:
            break

    gen_info = {l: t for l, t in zip(resultLabel, resultText)}
    jsonD = json.dumps(gen_info)

    return jsonD.decode('unicode_escape')

def get_requirements():
    # resultLabel = ['Квалификация', 'Требование']
    resultText = []
    page = urllib2.urlopen(link_page + '130452757')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        div = body.find('table', {'class': 'publicTableData'})
        for tbody in div.findAll('tbody'):
            for cell in tbody('td'):
                resultText.append(smart_str(cell.text))

    resultClass = resultText[1::3]
    resultReq = resultText[2::3]

    gen_info = [{'Квалификация': c, 'Требование': t} for c, t in zip(resultClass, resultReq)]
    jsonD = json.dumps(gen_info)
    return jsonD.decode('unicode_escape')

    # for div in body.findNextSiblings('table', {'class': 'publicTableData'}):

def get_criteria():
    resultText = []
    page = urllib2.urlopen(link_page + '130452757')
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

    gen_info = {l: t for l, t in zip(l, t)}
    jsonD = json.dumps(gen_info)
    return jsonD.decode('unicode_escape')

def get_special_require():
    resultLabel = []
    resultText = []
    # jsonD = []
    page = urllib2.urlopen(link_page + '130452757')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('div', {'class': 'container-content'})
        col = content.findNextSibling('div', {'class': 'container-content'})
        col1 = col.findNextSibling('div', {'class': 'container-content'})
        col2 = col1.findNextSibling('div', {'class': 'container-content'})
        for div in col2.findAll('div', {'class': 'col-12 col-md-6'}):
            for span in div.findAll('span', {'class': 'label'}):
                resultLabel.append(smart_str(span.text))
            for span1 in div.findAll('span', {'class': 'text'}):
                resultText.append(smart_str(span1.text))
        gen_info = {l: t for l, t in zip(resultLabel, resultText)}
        jsonD = json.dumps(gen_info)

    return jsonD.decode('unicode_escape')

def get_special_info():
    resultLabel = []
    resultText = []
    # jsonD = []
    page = urllib2.urlopen(link_page + '130452757')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('div', {'class': 'container-content'})
        col = content.findNextSibling('div', {'class': 'container-content'})
        col1 = col.findNextSibling('div', {'class': 'container-content'})
        col2 = col1.findNextSibling('div', {'class': 'container-content'})
        col3 = col2.findNextSibling('div', {'class': 'container-content'})
        col4 = col3.findNextSibling('div', {'class': 'container-content'})
        for div in col4.findAll('div', {'class': 'col-12 col-md-6'}):
            for span in div.findAll('span', {'class': 'label'}):
                resultLabel.append(smart_str(span.text))
            for span1 in div.findAll('span', {'class': 'text'}):
                resultText.append(smart_str(span1.text))
        gen_info = {l: t for l, t in zip(resultLabel, resultText)}
        jsonD = json.dumps(gen_info)

    return jsonD.decode('unicode_escape')

def get_pay_info():
    resultText = []
    page = urllib2.urlopen(link_page + '130452757')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        for div in body.findAll('div', {'class': 'row no-gutters'}):
            for tbody in div.findAll('tbody'):
                for cell in tbody('td'):
                    resultText.append(smart_str(cell.text))

    l = resultText[0::2]
    t = resultText[1::2]

    gen_info = {l: t for l, t in zip(l, t)}
    jsonD = json.dumps(gen_info)
    return jsonD.decode('unicode_escape')


# inserting the data to mongoDB
def inserting_to_DB():
    myclient = pymongo.MongoClient("192.168.0.166:27017")
    mydb = myclient["scrapping"]
    mycol = mydb["zakupki.gov.kg"]

    mydict = {"genInfo": get_general_info(), "OrganizationInfo": get_organization_info(), "lots": get_lots_info(),  "extralots": get_extralots_info(), "requirements": get_requirements(), "specRequirements": get_special_require(), "criteria": get_criteria(), "specialInfo": get_special_info(), "payInfo": get_pay_info()}

    x = mycol.insert_one(mydict)
    cursor = mycol.find()
    for record in cursor:
        print(record)

# finished
print get_general_info()
print "_________________"
print get_organization_info()

print "_________________"
print get_lots_info()
print "_________________"
print get_extralots_info()
print "_________________"
print get_requirements()
print "_________________"
print get_special_require()
print "_________________"
print get_criteria()
print "_________________"
print get_special_info()
print "_________________"
print get_pay_info()
print "_________________"

inserting_to_DB()


# for x in get_general_info():
#     print x.decode('unicode_escape')



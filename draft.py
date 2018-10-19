import urllib2

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
    page = urllib2.urlopen(link_page + '126401206')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('div', {'class': 'container-content'})
        # col = content.find('div', {'class': 'row'})
        for div in content.findAll('div', {'class': 'col-12 col-md-6'}):
            for span in div.findAll('span', {'class': 'label'}):
                resultLabel.append(smart_str(span.text))
            for span1 in div.findAll('span', {'class': 'text'}):
                resultText.append(smart_str(span1.text))
        gen_info = [{l: t} for l, t in zip(resultLabel, resultText)]
        jsonD = json.dumps(gen_info)

    return jsonD.decode('unicode_escape')


def get_organization_info():
    resultLabel = []
    resultText = []
    # jsonD = []
    page = urllib2.urlopen(link_page + '126401206')
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
        gen_info = [{l: t} for l, t in zip(resultLabel, resultText)]
        jsonD = json.dumps(gen_info)

    return jsonD.decode('unicode_escape')


def get_lots_info():
    lots = []
    page = urllib2.urlopen(link_page + '126401206')

    # driver = webdriver.Firefox()
    # driver.implicitly_wait(30)
    # driver.get(page)
    # button = driver.find_elements_by_class_name('.ui-row-toggler')
    # button.click()

    soup = BeautifulSoup(page, 'html.parser')
    # soup = BeautifulSoup(driver.page_source, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('span', {'class': 'field-groups-view m-left m-right'})
        for div in content.findAll('tbody', {'class': 'ui-datatable-data'}):
            resultText = div.prettify()
            for row in BeautifulSoup(resultText)('tr'):
                for cell in row('td'):
                    lots.append([cell.text])

    #     for span in cell.findAll('span'):
    #         resultLabel.append(smart_str(span.text))
    #     for span1 in cell.findAll('span', {'class': 'bold'}):
    #         resultText.append(smart_str(span1.text))
    # gen_info = [{l: t} for l, t in zip(resultLabel, resultText)]
    # jsonD = json.dumps(gen_info)

    jsonD = json.dumps(lots)

    return jsonD.decode('unicode_escape')

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
    time.sleep(6)

    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for body in soup.findAll('body'):
            content = body.find('span', {'class': 'field-groups-view m-left m-right'})
            for div in content.findAll('tbody', {'class': 'ui-datatable-data'}):
                resultText = div.prettify()
                for row in BeautifulSoup(resultText)('tr', {
                    'class': 'ui-expanded-row-content ui-widget-content childRowFillBG'}):
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
    return jsonD.decode('unicode_escape')


def get_requirements():
    resultLabel = []
    resultText = []
    lots = []
    page = urllib2.urlopen(link_page + '126401206')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        for div in body.findAll('table', {'class': 'publicTableData'}):
            # for thead in div.findAll('thead'):
            #     resultLabel.append(smart_str(thead.text))
            for tbody in div.findAll('tbody'):
                resultText.append(smart_str(tbody.text))
        # gen_info = [{"title": l, "value": t} for l, t in zip(resultLabel, resultText)]
        jsonD = json.dumps(resultText)
            # resultText = div.prettify()
            # lots.append([resultText.text])

    # jsonD = json.dumps(lots)

    return jsonD.decode('unicode_escape')

def get_special_require():
    resultLabel = []
    resultText = []
    # jsonD = []
    page = urllib2.urlopen(link_page + '126401206')
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
        gen_info = [{l: t} for l, t in zip(resultLabel, resultText)]
        jsonD = json.dumps(gen_info)

    return jsonD.decode('unicode_escape')

def get_special_info():
    resultLabel = []
    resultText = []
    # jsonD = []
    page = urllib2.urlopen(link_page + '126401206')
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
        gen_info = [{l: t} for l, t in zip(resultLabel, resultText)]
        jsonD = json.dumps(gen_info)

    return jsonD.decode('unicode_escape')

def get_pay_info():
    resultLabel = []
    resultText = []
    page = urllib2.urlopen(link_page + '126401206')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        for div in body.findAll('div', {'class': 'row no-gutters'}):
            # for thead in div.findAll('thead'):
            #     resultLabel.append(smart_str(thead.text))
            for tbody in div.findAll('tbody'):
                resultText.append(smart_str(tbody.text))
        # gen_info = [{"title": l, "value": t} for l, t in zip(resultLabel, resultText)]
        jsonD = json.dumps(resultText)

    return jsonD.decode('unicode_escape')


# print get_general_info()
# print get_organization_info()
print get_lots_info()
# print get_extralots_info()
# print get_requirements()
# print get_special_require()
# print get_special_info()
# print get_pay_info()

# for x in get_general_info():
#     print x.decode('unicode_escape')



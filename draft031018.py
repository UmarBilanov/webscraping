import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import re
import os
import urllib2
from bs4 import BeautifulSoup
from django.utils.encoding import smart_str
import json
# list_page = 'http://zakupki.gov.kg/popp/view/order/list.xhtml'
link_page = 'http://zakupki.gov.kg/popp/view/order/view.xhtml?id='




def get_data_rk():
    data_rk = []
    # page = urllib2.urlopen(list_page)
    url = "http://zakupki.gov.kg/popp/home.xhtml"

    # create a new Firefox session
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(url)
    button = driver.find_element_by_link_text('Advanced search')
    button.click()
    button = driver.find_element_by_xpath('//div[@id="tv1:status"]/ul')
    button.click()
    button = driver.find_element_by_xpath('//div[@id="tv1:status_panel"]/div[2]/ul/li/div/div[2]/span')
    button.click()
    button = driver.find_element_by_xpath('//div[@id="tv1:status_panel"]/div/a')
    button.click()
    button = driver.find_element_by_xpath('//div[@id="tv1:ate"]/ul')
    button.click()
    button = driver.find_element_by_xpath('//div[@id="tv1:ate_panel"]/div[2]/ul/li[6]/div/div[2]/span')
    button.click()
    button = driver.find_element_by_xpath('//div[@id="tv1:ate_panel"]/div/a')
    button.click()
    button = driver.find_element_by_xpath('//input[@name=\'tv1:j_idt152\']')
    button.click()


    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for tr in soup.findAll('tr', {'class': 'ui-widget-content'}):
            if 'data-rk' in tr.attrs:
                data_rk.append(tr["data-rk"])
        time.sleep(6)
        button = driver.find_element_by_xpath('//div[@id=\'j_idt104:j_idt105:table_paginator_bottom\']/a[3]')
        button.click()
        # print data_rk
        if 'ui-state-disabled' in button.get_attribute('class'):
            break
    # print data_rk
    return data_rk

print (get_data_rk())

def get_general_info():
    resultLabel = []
    resultText = []
    # jsonD = []
    page = urllib2.urlopen(link_page + list_id)
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        for content in body.findAll('div', {'class': 'container-content'}):
            for div in content.findAll('div', {'class': 'col-12 col-md-6'}):
                # jsonD = json.dumps(div.text)
                # resultText.append(jsonD)
                for span in div.findAll('span', {'class': 'label'}):
                    resultLabel.append(smart_str(span.text))
                for span1 in div.findAll('span', {'class': 'text'}):
                    resultText.append(smart_str(span1.text))
                gen_info = [{"title": l, "value": t} for l, t in zip(resultLabel, resultText)]
                jsonD = json.dumps(gen_info)
    return jsonD




for list_id in get_data_rk():
    print get_general_info().decode('unicode_escape')

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
    button = driver.find_element_by_xpath('//form[@id=\'tv1:j_idt84\']/div[2]/div/div/div/div[10]/input')
    button.click()
    # button = driver.find_elements_by_xpath('//div[@id=\'j_idt104:j_idt105:table_paginator_bottom\']/select')
    # button.click()
    # button = driver.find_element_by_id('j_idt104:j_idt105:table:j_id2')
    # button.select()
    # button = driver.find_elements_by_xpath('//select[@id=\'j_idt104:j_idt105:table:j_id2\']/option[5]')
    # button.click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    while True:
        for body in soup.findAll('tbody', {'class': 'ui-widget-content'}):
            for tr in body.findAll('tr'):
                if 'data-rk' in tr.attrs:
                    data_rk.append(tr["data-rk"])

        time.sleep(6)
        # button = driver.find_element_by_xpath('// div[ @ id = \'j_idt104:j_idt105:table_paginator_bottom\'] / a[4]')
        button = driver.find_element_by_xpath('//div[@id=\'j_idt104:j_idt105:table_paginator_bottom\']/a[3]')
        if 'ui-state-disabled' in button.get_attribute('class'):
            break
        button.click()

    return data_rk


        # try:
        #     time.sleep(6)
        #     button = driver.find_element_by_xpath('// div[ @ id = \'j_idt104:j_idt105:table_paginator_bottom\'] / a[4]')
        #     # button = driver.find_element_by_xpath('//div[@id=\'j_idt104:j_idt105:table_paginator_bottom\']/a[3]')
        #     button.click()
        # except:
        #     button = driver.find_element_by_class_name('ui-paginator-last ui-state-default ui-corner-all '
        #                                                'ui-state-disabled')
        #     button.close()
        # finally:
        #     print data_rk

print get_data_rk()

# ui-paginator-last ui-state-default ui-corner-all ui-state-disabled

def get_general_info():
    resultLabel = []
    resultText = []
    page = urllib2.urlopen(link_page + list_id)
    soup = BeautifulSoup(page, 'html.parser')
    for body in soup.findAll('body'):
        for content in body.findAll('div', {'class': 'container-content'}):
            for div in content.findAll('div', {'class': 'col-12 col-md-6'}):
                for span in div.findAll('span', {'class': 'label'}):
                    resultLabel.append(smart_str(span.text))
                for span1 in div.findAll('span', {'class': 'text'}):
                    resultText.append(smart_str(span1.text))
    # print resultLabel
    # print resultText
    #
    # for x in resultLabel:
    #     print x.decode('utf8')
    for y in resultText:
        print y.decode('utf8')


for list_id in get_data_rk():
    get_general_info()


# xpath=//div[@id="j_idt104:j_idt105:table_paginator_bottom"]/a[3]
# xpath = ( // a[contains( @ href, '#')])[33]
# button = driver.find_elements_by_xpath('//div[@id="j_idt104:j_idt105:table_paginator_bottom"]/a[3]')
#     button.click()

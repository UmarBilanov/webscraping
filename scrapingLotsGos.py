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
extralots = []
page = link_page + '126401206'

driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(page)
button = driver.find_element_by_link_text('RU')
button.click()

while True:
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(6)
        button = driver.find_element_by_xpath('//tbody[@id=\'j_idt69:lotsTable_data\']/tr/td[8]/div')
        button.click()
    except TimeoutException:
        break

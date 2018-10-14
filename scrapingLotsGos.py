import urllib2
from selenium import webdriver
from bs4 import BeautifulSoup
import xmltodict
import json
import pymongo

link_page = 'http://zakupki.gov.kg/popp/view/order/view.xhtml?id='

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

print jsonD.decode('unicode_escape')
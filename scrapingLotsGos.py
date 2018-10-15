import urllib2
from selenium import webdriver
from bs4 import BeautifulSoup
from collections import namedtuple
import xmltodict
import json
import pymongo

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
    genInfo =jsonD.decode('unicode_escape')

    print genInfo
    # return jsonD.decode('unicode_escape')

def get_lots_info():
    lots = []
    page = urllib2.urlopen(link_page + '126401206')

    soup = BeautifulSoup(page, 'html.parser')
    # soup = BeautifulSoup(driver.page_source, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('span', {'class': 'field-groups-view m-left m-right'})
        for div in content.findAll('tbody', {'class': 'ui-datatable-data'}):
            res = div.prettify()
    jsonD = json.dumps(xmltodict.parse(res))
    genInfo = jsonD.decode('unicode_escape')

    print genInfo

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

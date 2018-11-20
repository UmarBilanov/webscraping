# -*- coding: utf-8 -*-
import urllib2
import pymongo
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
import gridfs
import os
import re
import datetime

link_page = 'http://zakupki.gov.kg/popp/view/order/view.xhtml?id='
login_page = 'https://trade.okmot.kg/uac/view/user/login.xhtml'
link_page2 = 'https://trade.okmot.kg/sobs/view/bid/short_info.xhtml?id='
list_id = '134025360'

# def get_data_rk():
#     data_rk = []
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
#     while True:
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         for tr in soup.findAll('tr', {'class': 'ui-widget-content'}):
#             if 'data-rk' in tr.attrs:
#                 data_rk.append(tr["data-rk"])
#         time.sleep(6)
#         button = driver.find_element_by_xpath('//div[@id=\'j_idt104:j_idt105:table_paginator_bottom\']/a[3]')
#         button.click()
#         if 'ui-state-disabled' in button.get_attribute('class'):
#             break
#
#     # return data_rk

def get_general_info():
    resultLabel = []
    resultText = []

    page = urllib2.urlopen(link_page + list_id)
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('div', {'class': 'container-content'})
        for div in content.findAll('div', {'class': 'col-12 col-md-6'}):
            for span in div.findAll('span', {'class': 'label'}):
                resultLabel.append(span.text)
            for span1 in div.findAll('span', {'class': 'text'}):
                resultText.append(span1.text)
                # links = span1.find("a")
                # if links is not None:
                #     a = links.attrs['href']
    gen_info = {l: t for l, t in zip(resultLabel, resultText)}

    x = gen_info[u"Планируемая сумма"]
    y = x.encode('ascii', 'ignore')

    gen_info[u"Планируемая сумма"] = y

    # gen_info[u"Официальное информационное письмо по банковскому реквизиту"] = str(a)
    del gen_info[u"Дата публикации"]
    del gen_info[u"Срок подачи конкурсных заявок"]

    gen_info = {
        k.strip(): int(v)
        if v.isdigit()
        else v.strip()
        for k, v in gen_info.items()
        }

    json_file = open('/home/umar/PycharmProjects/WebscrapperDB/gen_info.json', 'w')
    json.dump(gen_info, json_file, indent=4)
    json_file.close()

    jsonD = json.dumps(gen_info, indent=4)
    return jsonD.decode('unicode_escape')

def get_organization_info():
    resultLabel = []
    resultText = []
    page = urllib2.urlopen(link_page + list_id)
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('div', {'class': 'container-content'}).findNextSibling('div',
                                                                                   {'class': 'container-content'})
        for div in content.findAll('div', {'class': 'col-12 col-md-6'}):
            for span in div.findAll('span', {'class': 'label'}):
                resultLabel.append(span.text)
            for span1 in div.findAll('span', {'class': 'text'}):
                resultText.append(span1.text)
    gen_info = {l: t for l, t in zip(resultLabel, resultText)}

    gen_info = {k.rstrip(): int(v) if v.isdigit() else v.rstrip() for k, v in gen_info.items()}

    json_file = open('/home/umar/PycharmProjects/WebscrapperDB/organization_info.json', 'w')
    json.dump(gen_info, json_file, indent=4)
    json_file.close()

    jsonD = json.dumps(gen_info, indent=4)
    return jsonD.decode('unicode_escape')

def get_lots_info():
    page = link_page + list_id
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
                        resultLabel.append(th.text)
                    for td in table('td'):
                        resultText.append(td.text)
                    lotsSpecs = [{l.strip(): int(t) if t.isdigit() else t.strip()} for l, t in zip(resultLabel, resultText)]

    list_of_lots = [lots[i:i + 5] for i in range(0, len(lots), 5)]

    list_of_spec = [lotsSpecs[i:i + 5] for i in range(0, len(lotsSpecs), 5)]

    gen_info = [{'№': l[0:i][0].strip(), 'Наименование лота': l[0:i][1].strip(), 'Сумма': int(l[0:i][2].encode('ascii', 'ignore')) if l[0:i][2].encode('ascii', 'ignore').isdigit() else l[0:i][2].encode('ascii', 'ignore').strip(), 'Адрес и Место поставки': l[0:i][3].strip(), 'Сроки поставки товара': l[0:i][4].strip(), 'techSpecifies': t} for l, t in zip(list_of_lots, list_of_spec)]
    jsonD = json.dumps(gen_info, indent=4)
    driver.close()

    json_file = open('/home/umar/PycharmProjects/WebscrapperDB/lots_info.json', 'w')
    json.dump(gen_info, json_file, indent=4)
    json_file.close()

    return jsonD.decode('unicode_escape')

def get_requirements():
    resultText = []
    page = urllib2.urlopen(link_page + list_id)
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        div = body.find('table', {'class': 'publicTableData'})
        for tbody in div.findAll('tbody'):
            for cell in tbody('td'):
                resultText.append(cell.text)

    resultClass = resultText[1::3]
    resultReq = resultText[2::3]

    gen_info = [{'Квалификация': c.strip(), 'Требование': t.strip()} for c, t in zip(resultClass, resultReq)]

    json_file = open('/home/umar/PycharmProjects/WebscrapperDB/requirements_info.json', 'w')
    json.dump(gen_info, json_file, indent=4)
    json_file.close()

    jsonD = json.dumps(gen_info, indent=4)
    return jsonD.decode('unicode_escape')

def get_criteria():
    resultText = []
    page = urllib2.urlopen(link_page + list_id)
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        div = body.find('table', {'class': 'publicTableData equal'})
        for tbody in div.findAll('tbody'):
            for cell in tbody('td'):
                resultText.append(cell.text)

    l = resultText[0::2]
    t = resultText[1::2]

    gen_info = {l.strip(): t.strip() for l, t in zip(l, t)}

    json_file = open('/home/umar/PycharmProjects/WebscrapperDB/criteria_info.json', 'w')
    json.dump(gen_info, json_file, indent=4)
    json_file.close()

    jsonD = json.dumps(gen_info, indent=4)
    return jsonD.decode('unicode_escape')

def get_special_require():
    resultLabel = []
    resultText = []
    page = urllib2.urlopen(link_page + list_id)
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('div', {'class': 'container-content'})
        col = content.findNextSibling('div', {'class': 'container-content'})
        col1 = col.findNextSibling('div', {'class': 'container-content'})
        col2 = col1.findNextSibling('div', {'class': 'container-content'})
        for div in col2.findAll('div', {'class': 'col-12 col-md-6'}):
            for span in div.findAll('span', {'class': 'label'}):
                resultLabel.append(span.text)
            for span1 in div.findAll('span', {'class': 'text'}):
                resultText.append(span1.text)

    gen_info = {l.strip(): t.strip() for l, t in zip(resultLabel, resultText)}

    json_file = open('/home/umar/PycharmProjects/WebscrapperDB/special_require.json', 'w')
    json.dump(gen_info, json_file, indent=4)
    json_file.close()

    jsonD = json.dumps(gen_info, indent=4)
    return jsonD.decode('unicode_escape')

def get_special_info():
    resultLabel = []
    resultText = []
    page = urllib2.urlopen(link_page + list_id)
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
                resultLabel.append(span.text)
            for span1 in div.findAll('span', {'class': 'text'}):
                resultText.append(span1.text)
    gen_info = {l.strip(): t.strip() for l, t in zip(resultLabel, resultText)}

    json_file = open('/home/umar/PycharmProjects/WebscrapperDB/special_info.json', 'w')
    json.dump(gen_info, json_file, indent=4)
    json_file.close()

    jsonD = json.dumps(gen_info, indent=4)
    return jsonD.decode('unicode_escape')

def get_pay_info():
    resultText = []
    page = urllib2.urlopen(link_page + list_id)
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        for div in body.findAll('div', {'class': 'row no-gutters'}):
            for tbody in div.findAll('tbody'):
                for cell in tbody('td'):
                    resultText.append(cell.text)

    l = resultText[0::2]
    t = resultText[1::2]

    gen_info = {l: t for l, t in zip(l, t)}
    # del gen_info[u"Место предполагаемого тех. контроля и испытаний"]

    jsonD = json.dumps(gen_info)

    json_file = open('/home/umar/PycharmProjects/WebscrapperDB/pay_info.json', 'w')
    json.dump(gen_info, json_file, indent=4)
    json_file.close()

    return jsonD.decode('unicode_escape')

def get_files():
    page2 = link_page2 + list_id
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", '/home/umar/PycharmProjects/WebscrapperDB')
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/octet-stream')

    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get(login_page)
    time.sleep(6)
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys("askartec")
    time.sleep(5) #sleep_mini sleep_norm sleep_max sleep_long
    password.send_keys("@BigMama2013")
    time.sleep(5)
    login = driver.find_element_by_xpath("//input[@value='Войти']")
    login.click()
    time.sleep(10)
    driver.get(page2)
    time.sleep(10)
    button = driver.find_element_by_id('downloadLink')
    button.click()

    driver.close()

def inserting_to_mongoDB():
    # we are getting the json and attached files
    get_general_info()
    get_organization_info()
    get_lots_info()
    get_requirements()
    get_criteria()
    get_special_require()
    get_special_info()
    get_pay_info()
    get_files()
    # we are getting the json and attached files

    # getting the name of attached zip file
    resultLabel = []
    resultText = []

    page = urllib2.urlopen(link_page + '134025360')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('div', {'class': 'container-content'})
        for div in content.findAll('div', {'class': 'col-12 col-md-6'}):
            for span in div.findAll('span', {'class': 'label'}):
                resultLabel.append(span.text)
            for span1 in div.findAll('span', {'class': 'text'}):
                resultText.append(span1.text)

    gen_info = {l: t for l, t in zip(resultLabel, resultText)}

    x = gen_info[u"Номер"]
    t = gen_info[u"Наименование закупки"]
    y = x.encode('ascii', 'ignore') + '.zip'

    filename = str(y)
    NamePurchase = t
    # getting the name of attached zip file

    # converting string Date to date
    a = gen_info[u"Дата публикации"]
    b = gen_info[u"Срок подачи конкурсных заявок"]
    d = str(a.encode('utf-8'))
    # f = d.replace("ноября", "11")
    e = str(b.encode('utf-8'))

    # replacing the string name of  month to number of month
    rep = {"января": "01", "февраля": "02", "марта": "03", "апреля": "04", "мая": "05", "июня": "06", "июля": "07",
           "августа": "08", "сентября": "09", "октября": "10", "ноября": "11",
           "декабря": "12"}  # define desired replacements here

    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    d = pattern.sub(lambda m: rep[re.escape(m.group(0))], d)
    e = pattern.sub(lambda m: rep[re.escape(m.group(0))], e)
    # replacing the string name of  month to number of month

    print d
    print type(d)
    PDate = datetime.datetime.strptime(d, "%d %m %Y %H:%M")
    FinalDate = datetime.datetime.strptime(e, "%d %m %Y %H:%M")
    print PDate
    print FinalDate
    # converting string Date to date

    # connecting to mongoDB
    myclient = pymongo.MongoClient("localhost:27017")
    mydb = myclient["scrapping"]
    mycol = mydb["zakupki.gov.kg"]
    # connecting to mongoDB

    # inserting the archive to mongoDB
    fs = gridfs.GridFS(mydb)
    fileID = fs.put(open(r'/home/umar/PycharmProjects/WebscrapperDB/' + filename, 'r'), filename='AttachedFiles.zip')
    out = fs.get(fileID)
    print out.length
    print out.filename
    # inserting the archive to MongoDB

    # inserting the files and and archive to MongoDB
    with open('/home/umar/PycharmProjects/WebscrapperDB/gen_info.json') as f:
        general_data = json.load(f)

    with open('/home/umar/PycharmProjects/WebscrapperDB/organization_info.json') as f:
        organization_data = json.load(f)

    with open('/home/umar/PycharmProjects/WebscrapperDB/lots_info.json') as f:
        lots_data = json.load(f)

    with open('/home/umar/PycharmProjects/WebscrapperDB/requirements_info.json') as f:
        requirements_data = json.load(f)

    with open('/home/umar/PycharmProjects/WebscrapperDB/criteria_info.json') as f:
        criteria_data = json.load(f)

    with open('/home/umar/PycharmProjects/WebscrapperDB/special_require.json') as f:
        special_require_data = json.load(f)

    with open('/home/umar/PycharmProjects/WebscrapperDB/special_info.json') as f:
        special_data = json.load(f)

    with open('/home/umar/PycharmProjects/WebscrapperDB/pay_info.json') as f:
        pay_data = json.load(f)

    result_data = {
        "Наименование закупки": NamePurchase,
        "Дата публикации": PDate,
        "Срок подачи конкурсных заявок": FinalDate,
        "Общие данные": general_data,
        "Информация об организации": organization_data,
        "Лоты": lots_data,
        "Квалификационные требования": requirements_data,
        "Критерии оценки конкурсных заявок": criteria_data,
        "Специальные требования": special_require_data,
        "Особые условия договора": special_data,
        "Об условия оплаты": pay_data,
        "Приклепленые файлы": out._id
    }

    mycol.remove()
    mycol.insert(result_data, check_keys=False)
    # inserting the files and and archive to MongoDB
    myclient.close()

    # deleting the all files in folder
    folder = '/home/umar/PycharmProjects/WebscrapperDB'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    # deleting the files in folder

inserting_to_mongoDB()
# for list_id in get_data_rk():
#     inserting_to_mongoDB()
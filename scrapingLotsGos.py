# -*- coding: utf-8 -*-
import urllib2
import pymongo
from django.utils.encoding import smart_str
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
import zipfile
import shutil
import gridfs
import os
import re
import datetime

link_page = 'http://zakupki.gov.kg/popp/view/order/view.xhtml?id='

def get_general_info():
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
                links = span1.find("a")
                if links is not None:
                    a = links.attrs['href']
    gen_info = {l: t for l, t in zip(resultLabel, resultText)}

    # del gen_info[u"Размер гарантийного обеспечения конкурсной заявки (ГОКЗ): Декларация"]

    # Get the file name for the new file to write
    # with open('gen_info.json', 'w') as outfile:
    #     json.dump(gen_info, outfile)

    x = gen_info[u"Планируемая сумма"]
    y = x.encode('ascii', 'ignore')

    gen_info[u"Планируемая сумма"] = y
    # print y

    # del gen_info[u"Дата публикации"]
    # del gen_info[u"Срок подачи конкурсных заявок"]

    gen_info[u"Официальное информационное письмо по банковскому реквизиту"] = str(a)

    gen_info = {
        k.strip(): int(v)
        if v.isdigit()
        else v.strip()
        for k, v in gen_info.items()
        }
    # x.replace('y', '')
    # y = str(x)
    # resultr = re.sub(ur'u"\u0020"', '', x)
    # ord(u'\ua000')
    # x = u''.join(gen_info[u"Планируемая сумма"]).encode('utf-8').strip(' ')
    json_file = open('/home/umar/PycharmProjects/WebscrapperDB/gen_info.json', 'w')
    json.dump(gen_info, json_file, indent=4)
    json_file.close()

    jsonD = json.dumps(gen_info, indent=4)
    return jsonD.decode('unicode_escape')

def get_organization_info():
    resultLabel = []
    resultText = []
    # jsonD = []
    page = urllib2.urlopen(link_page + '134025360')
    soup = BeautifulSoup(page, 'html.parser')

    for body in soup.findAll('body'):
        content = body.find('div', {'class': 'container-content'}).findNextSibling('div',
                                                                                   {'class': 'container-content'})
        # col = content.find('div', {'class': 'row'}).next_sibling('div', {'class': 'row'})
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
    page = link_page + '134025360'
    lots = []
    resultText = []
    resultLabel = []
    list_of_files = []

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

            for row in div.findAll('tr', {'class': 'ui-expanded-row-content ui-widget-content childRowFillBG'}):
                for table in row.findAll('table', {'class': 'display-table private-room-table no-borders f-right'}):
                    for td in table('td'):
                        for links in td.findAll("a"):
                            if links is not None:
                                a = links.attrs['href']
                                list_of_files.append(a)

    list_of_lots = [lots[i:i + 5] for i in range(0, len(lots), 5)]
    # l[0:i][2] = [l[0:i][2].encode('ascii', 'ignore') for l in zip(list_of_lots)]

    list_of_spec = [lotsSpecs[i:i + 5] for i in range(0, len(lotsSpecs), 5)]
    # print list_of_spec

    # print list_of_files

    gen_info = [{'№': l[0:i][0].strip(), 'Наименование лота': l[0:i][1].strip(), 'Сумма': int(l[0:i][2].encode('ascii', 'ignore')) if l[0:i][2].encode('ascii', 'ignore').isdigit() else l[0:i][2].encode('ascii', 'ignore').strip(), 'Адрес и Место поставки': l[0:i][3].strip(), 'Сроки поставки товара': l[0:i][4].strip(), 'techSpecifies': t, 'Файл': f} for l, t, f in zip(list_of_lots, list_of_spec, list_of_files)]
    jsonD = json.dumps(gen_info, indent=4)
    driver.close()

    json_file = open('/home/umar/PycharmProjects/WebscrapperDB/lots_info.json', 'w')
    json.dump(gen_info, json_file, indent=4)
    json_file.close()

    return jsonD.decode('unicode_escape')

def get_special_info():
            resultLabel = []
            resultText = []
            # jsonD = []
            page = urllib2.urlopen(link_page + '134025360')
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

                json_file = open('/home/umar/PycharmProjects/WebscrapperDB/special_info.json', 'w')
                json.dump(gen_info, json_file, indent=4)
                json_file.close()

            return jsonD.decode('unicode_escape')

def get_pay_info():
            resultText = []
            page = urllib2.urlopen(link_page + '134025360')
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
    # file_page = 'https://trade.okmot.kg/sobs/view/bid/short_info.xhtml?id=134025360'

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", '/home/umar/PycharmProjects/WebscrapperDB')
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/octet-stream')

    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get("https://trade.okmot.kg/uac/view/user/login.xhtml")
    time.sleep(6)
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys("askartec")
    time.sleep(5) #sleep_mini sleep_norm sleep_max sleep_long
    password.send_keys("@BigMama2013")
    time.sleep(5)
    login = driver.find_element_by_xpath("//input[@value='Войти']")
    login.click()
    time.sleep(5)
    driver.get("https://trade.okmot.kg/sobs/view/bid/short_info.xhtml?id=134025360")
    time.sleep(10)
    button = driver.find_element_by_id('downloadLink')
    button.click()

    driver.close()

def inserting_to_mongoDB():
    # we are getting the json and attached files
    get_general_info()
    get_organization_info()
    get_lots_info()
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

    with open('/home/umar/PycharmProjects/WebscrapperDB/special_info.json') as f:
        special_data = json.load(f)

    with open('/home/umar/PycharmProjects/WebscrapperDB/pay_info.json') as f:
        pay_data = json.load(f)

    result_data = {
        "Наименование закупки": NamePurchase,
        "Дата публикации": PDate,
        "Срок подачи конкурсных заявок": FinalDate,
        "General info": general_data,
        "Organization info": organization_data,
        "Lots info": lots_data,
        "Special info": special_data,
        "Pay info": pay_data,
        "Attached files": out._id
    }

    # mycol.remove()
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

def inserting_to_GridFS():
    # we are getting the json and attached files
    get_general_info()
    get_organization_info()
    get_lots_info()
    get_special_info()
    get_pay_info()
    get_files()
    # we are getting the json and attached files

    # getting the name of attached zip file
    resultLabel = []
    resultText = []

    page = urllib2.urlopen(link_page + '130452757')
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
    y = x.encode('ascii', 'ignore') + '.zip'
    z = x.encode('ascii', 'ignore')

    filename = str(y)
    fileName = str(z)
    print filename
    # getting the name of attached zip file

    # extracting the zipped file
    with zipfile.ZipFile(r'/home/umar/PycharmProjects/WebscrapperDB/' + filename, 'r') as Zip:
        # extracting all the files
        Zip.extractall('/home/umar/PycharmProjects/WebscrapperDB')
    # extracting the zipped file

    # removing the downloaded zip file
    os.remove(r'/home/umar/PycharmProjects/WebscrapperDB/' + filename)
    # removing the downloaded zip file

    # making the folder archive
    shutil.make_archive('/home/umar/PycharmProjects/' + fileName, 'zip', '/home/umar/PycharmProjects/', 'WebscrapperDB')
    # making the folder archive

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

    # moving the archive file
    shutil.move('/home/umar/PycharmProjects/' + filename, '/home/umar/PycharmProjects/WebscrapperDB/' + filename)
    # moving the archive file

    # connecting to mongoDB
    myclient = pymongo.MongoClient("localhost:27017")
    mydb = myclient["scrapping"]
    # connecting to mongoDB

    # inserting the archive to mongoDB
    fs = gridfs.GridFS(mydb)
    fileID = fs.put(open(r'/home/umar/PycharmProjects/WebscrapperDB/' + filename, 'r'))
    out = fs.get(fileID)
    print out.length
    print out.read()
    # inserting the archive to mongoDB

# def geting_lots_info():
#     resultLabel = ['№', 'Наименование лота', 'Сумма', 'Адрес и Место поставки', 'Сроки поставки товара ']
#     resultText = []
#     gen_info = {}
#     page = urllib2.urlopen(link_page + '130452757')
#
#     soup = BeautifulSoup(page, 'html.parser')
#     # soup = BeautifulSoup(driver.page_source, 'html.parser')
#
#     for body in soup.findAll('body'):
#         content = body.find('span', {'class': 'field-groups-view m-left m-right'})
#         for div in content.findAll('tbody', {'class': 'ui-datatable-data'}):
#             for row in div('tr'):
#                 for cell in row('td'):
#                     for span in cell.findAll('span', {'class': 'bold'}):
#                         resultText.append(span.text)
#
#     list_of_lists = [resultText[i:i + 5] for i in range(0, len(resultText), 5)]
#     # jsonT = json.dumps(list_of_lists)
#     # print jsonT.decode('unicode_escape')
#
#     list_of_lists.append(resultLabel)
#     # jsonL = json.dumps(list_of_lists)
#     # print jsonL.decode('unicode_escape')
#     l = len(list_of_lists)
#     gen_info = {z[l-1]: list(z[0:l-2]) for z in zip(*list_of_lists)}
#
#     # gen_info = [{z[0]: list(z[1:])} for z in zip(resultLabel, list_of_texts)]
#     jsonD = json.dumps(gen_info)
#     return jsonD.decode('unicode_escape')
#
# def get_extralots_info():
#     # lots = []
#     resultLabel = []
#     resultText = []
#     # data_ri = []
#     page = link_page + '128014811'
#
#     driver = webdriver.Firefox()
#     driver.implicitly_wait(30)
#     driver.get(page)
#     button = driver.find_element_by_link_text('RU')
#     button.click()
#
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     # soup = BeautifulSoup(driver.page_source, 'html.parser')
#
#     for body in soup.findAll('body'):
#         content = body.find('span', {'class': 'field-groups-view m-left m-right'})
#         for div in content.findAll('tbody', {'class': 'ui-datatable-data ui-widget-content'}):
#             last_tr = div.find_all('tr')[-1]
#             if 'data-ri' in last_tr.attrs:
#                 tr_num = last_tr["data-ri"]
#     last_num = int(tr_num)
#     # print last_num
#     d = last_num * 2 + 1
#
#     x = 1
#     b = str(d)
#     time.sleep(5)
#
#     while True:
#         a = str(x)
#         time.sleep(6)
#         xpath = '//tbody[@id="j_idt69:lotsTable_data"]/tr[' + a + ']/td[8]/div'
#         button = driver.find_element_by_xpath(xpath)
#         button.click()
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         x += 2
#         for body in soup.findAll('body'):
#             content = body.find('span', {'class': 'field-groups-view m-left m-right'})
#             for div in content.findAll('tbody', {'class': 'ui-datatable-data'}):
#                 for row in div.findAll('tr', {'class': 'ui-expanded-row-content ui-widget-content childRowFillBG'}):
#                     for table in row.findAll('table', {'class': 'display-table private-room-table no-borders f-right'}):
#                         for th in table('th'):
#                             resultLabel.append(smart_str(th.text))
#                         for td in table('td'):
#                             resultText.append(smart_str(td.text))
#         if a == b:
#             break
#
#     gen_info = [{l: t} for l, t in zip(resultLabel, resultText)]
#     jsonD = json.dumps(gen_info)
#
#     return jsonD.decode('unicode_escape')


# print get_general_info()
# print get_organization_info()
# print get_lots_info()
# print get_special_info()
# print get_pay_info()
# get_general_info()
# get_organization_info()
# get_lots_info()
# get_special_info()
# get_pay_info()
inserting_to_mongoDB()

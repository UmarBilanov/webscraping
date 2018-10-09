# import libraries
import urllib2
from bs4 import BeautifulSoup

# specify the url
quote_page = 'http://www.link.kg/catalog/16/'

page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

title_site = soup.find('title')
title = title_site.text
print title

name_box = soup.find('tr')
name = name_box.text
print name

price_box = soup.find_all('td', attrs={'class': 'tp'})
print price_box
# price = price_box
# print price

# import libraries
import urllib2
from bs4 import BeautifulSoup

# specify the url
quote_page = 'http://enter.kg/computers/ultrabuki_bishkek'

page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

name_box = soup.find('span', attrs={'class': 'prouct_name'})
name = name_box.text
print name

price_box = soup.find('span', attrs={'class': 'price'})
price = price_box.text
print price

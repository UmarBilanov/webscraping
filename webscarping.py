# import libraries
import urllib2

from bs4 import BeautifulSoup

# specify the url
quote_page = 'http://www.bloomberg.com/quote/SPX:IND'


page = urllib2.urlopen(quote_page)
# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')
# soup = BeautifulSoup(page.text, 'html.parser')
# name = soup.find(class_:'companyName__99a4824b')
# Take out the <div> of name and get its value
name_box = soup.find_all('h1', attrs={'class': 'companyName__99a4824b'})
print name_box
# name = name_box.text.strip()
# strip() is used to remove starting and trailing
# print name
# get the index price
price_box = soup.find('span', attrs={'class': 'priceText__1853e8a5'})
print price_box

price = soup.find('span', class_ = 'priceText__1853e8a5')

# price = price.text
print(price)
# price = price_box.text
# print price

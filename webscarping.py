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
#
# directory = '/home/umar/PycharmProjects/WebscrapperDB'
#
#     # calling function to get all file paths in the directory
#     file_paths = []
#
#     # crawling through directory and subdirectories
#     for root, directories, files in os.walk(directory):
#         for filename in files:
#             # join the two strings in order to form the full filepath.
#             filepath = os.path.join(root, filename)
#             file_paths.append(filepath)
#
#             # printing the list of all files to be zipped
#     print('Following files will be zipped:')
#     for file_name in file_paths:
#         print(file_name)
#
#         # writing files to a zipfile
#     with zipfile(r'/home/umar/PycharmProjects/WebscrapperDB/' + filename, 'w') as Zip:
#         # writing each file one by one
#         for file in file_paths:
#             Zip.write(file)
#
#     print('All files zipped successfully!')

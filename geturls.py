# Made for the IMDb search pages
from lxml import html
import requests
import sys

with open(sys.argv[1]) as FILE:
    searches = FILE.readlines()
    FILE.close()

pages = int(sys.argv[2])
urls = []
for numSearches in range(0, len(searches)):
    
    for numPages in range(0, pages):
        if numPages != 0:
           
            if numPages > 1:
                newSearch = ''.join(tree.xpath('//*[@id="main"]/div/div/div[4]/div/a[2]/@href'))
            else:
                newSearch = ''.join(tree.xpath('//*[@id="main"]/div/div/div[4]/div/a/@href'))
            newSearch = str('http://www.imdb.com/search/title%s' % newSearch)
            searches[numSearches] = newSearch
        
        print(searches[numSearches])
        page = requests.get(searches[numSearches])
        tree = html.fromstring(page.content)
        
        for i in range (1, 51):
            urls.append(tree.xpath('//*[@id="main"]/div/div/div[3]/div[' + str(i) + ']/div[3]/h3/a/@href'))


for i in range(0, len(urls)):
    with open(sys.argv[3], "a+") as wFILE:
        urls[i] = ''.join(urls[i])
        wFILE.write("http://www.imdb.com%s\n" % urls[i])
wFILE.close()
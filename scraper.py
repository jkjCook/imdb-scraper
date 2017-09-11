from lxml import html
import requests
import sys
import json

# Input your URLs to the variable using a text file on the command line

with open(sys.argv[1]) as FILE:
    urls = FILE.readlines()

# Input original top level JSON brace
with open(sys.argv[2], 'a+') as wFILE:
    wFILE.write("[")
    wFILE.close()

for index in range (0, len(urls)): 

    # Sets your request to the URLs inside of the text document

    page = requests.get(urls[index])
    tree = html.fromstring(page.content)
    d = {}
                        
    title = tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/h1/text()')
    title = ''.join(title).lstrip().rstrip()
    if title == "":
        title = tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div/div[2]/h1/text()')
        title = ''.join(title).lstrip().rstrip()
    d['title'] = title

    year = tree.xpath('//*[@id="titleYear"]/a/text()')
    year = ''.join(year).lstrip()
    d['year'] = year

    runtime = tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/div/time/text()')
    runtime = ''.join(runtime).lstrip().rstrip()
    d['runtime'] = runtime

    genres = []
    for i in range(1, 4):
        if tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/div/a[' + str(i) + ']/span/text()'):
            genres.append(tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/div/a[' + str(i) + ']/span/text()'))
    d['genres'] = genres

    userRating = tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()')
    userRating = ''.join(userRating).lstrip()
    d['userRating'] = userRating

    # For newer layouts of IMDb
    if tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[3]/div[2]/a/img'):

        poster = tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[3]/div[1]/a/img/@src')
        poster = ''.join(poster).lstrip()
        d['poster'] = poster

        metaScore = tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[2]/div[1]/a/div/span/text()')
        metaScore = ''.join(metaScore).lstrip()
        d['metaScore'] = metaScore

        synopsis = tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[1]/text()')
        synopsis = ''.join(synopsis).lstrip().rstrip()
        d['synopsis'] = synopsis

        director = tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[2]/span/a/span/text()')
        director = ''.join(director).lstrip()
        d['director'] = director

        writers = []
        for i in range(1, 4):
            if tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[3]/span[' + str(i) +']/a/span/text()'):
                writers.append(tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[3]/span[' + str(i) +']/a/span/text()'))
            
           
        d['writers'] = writers
        
        stars = []
        for i in range (1, 4):
            if tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[4]/span['+ str(i) +']/a/span/text()'):
                stars.append(tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[4]/span['+ str(i) +']/a/span/text()'))
        d['stars'] = stars

        trailer = tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[3]/div[2]/a/@data-video')
        trailer = ''.join(trailer).lstrip().rstrip()
        trailer = str('http://www.imdb.com/videoembed/' + trailer)
        d['trailer'] = trailer
    
    # For older layouts of IMDb
    else:
        poster = tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/a/img/@src')
        poster = ''.join(poster).lstrip()
        d['poster'] = poster

        metaScore = tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[2]/div[2]/div[1]/a/div/span/text()')
        metaScore = ''.join(metaScore).lstrip()
        d['metaScore'] = metaScore

        synopsis = tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[2]/div[2]/div[1]/a/div/span/text()')
        synopsis = ''.join(synopsis).lstrip().rstrip()
        d['synopsis'] = synopsis

        director = tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[2]/div[1]/div[2]/span/a/span/text()')
        director = ''.join(director).lstrip()
        d['director'] = director

        writers = []
        for i in range(1, 4):
            if tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[2]/div[1]/div[3]/span[' + str(i) + ']/a/span/text()'):
                writers.append(tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[2]/div[1]/div[3]/span[' + str(i) + ']/a/span/text()'))
            
        d['writers'] = writers

        stars = []
        for i in range (1, 4):
            if tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[2]/div[1]/div[4]/span[' + str(i) + ']/a/span/text()'):
                stars.append(tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[2]/div[1]/div[4]/span[' + str(i) + ']/a/span/text()'))
        d['stars'] = stars

        d['trailer'] = 'N/A'

    # Dump dictionary to JSON file
    with open(sys.argv[2], 'a+') as wFILE:
        json.dump(d, wFILE)
        if index != len(urls) - 1:
            wFILE.write(',')
        wFILE.close()
    
# Close JSON
with open(sys.argv[2], 'a+') as wFILE:
    wFILE.write("]")
    wFILE.close()


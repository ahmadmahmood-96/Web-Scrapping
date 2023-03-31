import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as requests
import re

books = []
headings = []
details = []
authors = []
wiki_dates = []
dates = []
genres = []
wiki_genre = []
links = []

response = requests.get("https://entertainment.time.com/2005/10/16/all-time-100-novels/slide/all/").text
soup = bs(response, "html.parser")
names = soup.findAll("i")

for name in names:
    books.append(name.text)

books = books[0:90]

base_url = 'https://en.wikipedia.org/wiki/'

for book in books:
    link = base_url + book
    responseLink = requests.get(link).url
    links.append(responseLink)

    responseText = requests.get(link).text
    soup1 = bs(responseText, "html.parser")
    info = soup1.findAll("table", class_="infobox")

    headings.clear()
    details.clear()
    for i in info:
        h = i.findAll('tr')
        for j in h:
            heading = j.findAll('th')
            detail = j.findAll('td')
            if heading is not None and detail is not None:
                for x, y in zip(heading, detail):
                    headings.append(x.text)
                    details.append(y.text)
        break

    indexA = -1
    checkA = True
    for author in headings:
        indexA = indexA + 1
        if author == "Author":
            checkA = False
            authors.append(details[indexA])
            break
    if checkA:
        authors.append("Not Specified")

    checkG = True
    indexG = -1
    for genre in headings:
        indexG = indexG + 1
        if genre == "Genre" or genre == "Subject":
            checkG = False
            wiki_genre.append(details[indexG])
            break
    if checkG:
        wiki_genre.append("Not Specified")

    checkD = True
    indexD = -1
    for date in headings:
        indexD = indexD + 1
        if date == "Published" or date == "Published date" or date == "Date" or date == "Publication date":
            checkD = False
            wiki_dates.append(details[indexD])
            break
    if checkD:
        wiki_dates.append("Not Specified")

pattern = re.compile(r'\d{4}|\bNot\sSpecified')
for date in wiki_dates:
    matches = pattern.search(date)
    dates.append(matches.group())

for genre in wiki_genre:
    match = re.sub(r'\n|[\[0-9]]|[\[\]]', "", genre)
    genres.append(match)

dataframe = pd.DataFrame({'Book': books, 'Author': authors, 'Genre': genres, 'Publishing Year': dates, 'Link': links})
print(dataframe)

web = {}
for a, b, g, d, l in zip(authors, books, genres, dates, links):
    web[b] = [a, g, d, l]

count = 0
print("%-40s%-27s%-92s%-20s%-10s" % ("Book", "Author", "Genre", "Publishing Year", "Link"))
for k in web.keys():
    val = web[k]
    if val[0] != "Not Specified" and val[1] != "Not Specified" and val[3] != "Not Specified":
        count = count + 1
        print("%-40s%-27s%-92s%-20s%-10s" % (k, val[0], val[1], val[2], val[3]))


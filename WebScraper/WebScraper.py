import requests
from bs4 import BeautifulSoup
import re
import spacy
import numpy
from pandas import DataFrame
import matplotlib.pyplot as plt
import pandas as pd

result = requests.get("https://www.news.de/panorama/855829645/coronavirus-news-zu-ausbreitung-von-covid-19-in-deutschland-zahlen-ueber-"
                      "20-000-infizierte-polizei-warnt-in-corona-krise-vor-betruegern/1/")

nlp = spacy.load("de_core_news_md")

src = result.content
soup = BeautifulSoup(src, 'lxml')

#dates = re.findall(r'[\d]{1,2}[.][\d]{1,2}[.][\d]{4}', result.text)


start_date = []
end_date = []
location = []
organisation = []
persons = []
measure_type = []

for h2 in soup.find_all("h2"):
    date = re.findall(r'[\d]{1,2}[.][\d]{1,2}[.][\d]{4}', h2.text)
    if(date):
        start_date.append(date)
    else:
        start_date.append("NONE")

    foo = re.sub('[^A-Za-zäÄöÖüÜß]+', ' ', h2.text)
    print(foo)
    clean = h2.text.strip("+")
    doc = nlp(foo)


    for entity in doc.ents:
        print(entity.label_, ' | ', entity.text)

        if(entity.label_ == "LOC"):
            location.append(entity.text)
        else:
            location.append(numpy.nan)

        if (entity.label_ == "PER"):
            persons.append(entity.text)
        else:
            persons.append(numpy.nan)

        if (entity.label_ == "ORG"):
            organisation.append(entity.text)
        else:
            organisation.append(numpy.nan)

while len(start_date) > 234:
    start_date.pop()

print(len(location))
print(len(date))

#for l in range(len(start_date)):
    #print(start_date[l] + location[l] + persons[l] + organisation[l])

for idx, l in enumerate(start_date):
    print(start_date[idx],' | ', location[idx],' | ', persons[idx], ' | ',organisation[idx])


#df = [start_date, end_date,location, organisation, persons,measure_type]
#df['Occupation'].value_counts().plot(kind='pie', title='Occupation')
#plt.show()
#print(len(dates))

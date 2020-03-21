import requests
from bs4 import BeautifulSoup
import re
import spacy

result = requests.get("https://www.news.de/panorama/855829645/coronavirus-news-zu-ausbreitung-von-covid-19-in-deutschland-zahlen-ueber-"
                      "20-000-infizierte-polizei-warnt-in-corona-krise-vor-betruegern/1/")
nlp = spacy.load("de_core_news_md")

src = result.content

soup = BeautifulSoup(src, 'lxml')

dates = re.findall(r'[\d]{1,2}[.][\d]{1,2}[.][\d]{4}', result.text)

for h2 in soup.find_all("h2"):
    foo = re.sub('[^A-Za-zäÄöÖüÜß]+', ' ', h2.text)
    print(foo)
    clean =  h2.text.strip("+")
    doc = nlp(foo)
    for entity in doc.ents:
        print(entity.label_, ' | ', entity.text)


print(len(dates))

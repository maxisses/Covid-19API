from bs4 import BeautifulSoup
import re
import spacy
import numpy
from pandas import DataFrame
import pandas as pd
import requests
from datetime import datetime

def scrape_something():
    result = requests.get("https://www.news.de/panorama/855829645/coronavirus-news-zu-ausbreitung-von-covid-19-in-deutschland-zahlen-ueber-"
                        "20-000-infizierte-polizei-warnt-in-corona-krise-vor-betruegern/1/")

    nlp = spacy.load("de_core_news_sm")

    src = result.content

    soup = BeautifulSoup(src, 'lxml')

    
    rows = []
    for h2 in soup.find_all("h2"):
        start_date = []
        date = re.findall(r'[\d]{1,2}[.][\d]{1,2}[.][\d]{4}', h2.text)
        if(date):
            start_date.append(date)
        else:
            start_date.append("None")
            
        for dates in start_date:
            if dates != "None":
                try:
                    selected_date = datetime.strptime(str(dates[0]), "%d.%m.%Y").date()
                except:
                    selected_date = "unbekannt"
            else:
                selected_date = "unbekannt"
                
        
        foo = re.sub('[^A-Za-zäÄöÖüÜß]+', ' ', h2.text)
        #print(foo)
        clean =  h2.text.strip("+")
        clean = h2.text.strip("+")
        doc = nlp(foo)
        
        location = []
        person = []
        organisation = []
        for entity in doc.ents:
            #print(entity.label_, ' | ', entity.text)
            if(entity.label_ == "LOC"):
                location.append(entity.text)
            else:
                location.append(numpy.nan)

            if (entity.label_ == "ORG"):
                organisation.append(entity.text)
            else:
                organisation.append(numpy.nan)
        
        rows.append([datetime.now(), selected_date, foo, location, organisation])

    df = pd.DataFrame(rows)
    df.columns = ["extraction_date", "referred_date", "description", "location", "organisation"]
    return rows

print(scrape_something())






import time
import sys

import psycopg2
import psycopg2.extras

from bs4 import BeautifulSoup

#import numpy
#from pandas import DataFrame
#import pandas as pd
import requests
import re
from datetime import datetime,  timedelta

import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, EntitiesOptions

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
### to run with a remote docker image
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def check_scraped_urls(dbparams):

    dbname = dbparams.get('DB_DATABASE')
    dbuser = dbparams.get('DB_USER')
    dbpassword = dbparams.get('DB_PASSWORD')
    dbhost = dbparams.get('DB_HOST')
    dbport = dbparams.get('DB_PORT')

    conn = None
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, port=dbport, password=dbpassword)

        cur = conn.cursor()

        query = """
            SELECT DISTINCT news_url from corona_events_tagesschau
            """
        cur.execute(query)
        scraped_urls = cur.fetchall()
        scraped_urls = [item[0] for item in scraped_urls]
        print(f"--- {len(scraped_urls)} urls (days) already in the DB ----")

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
    
    return scraped_urls

def get_active_urls():
    urls = []
    current_dates = []
    today = datetime.now().strftime('%Y-%m-%d')
    weekend_days = ["montag","dienstag","mittwoch","donnerstag", "freitag", "samstag", "sonntag"]
    for i in range(100,199,1):
        current_checker = str(i)
        current_url = f"https://www.tagesschau.de/newsticker/liveblog-coronavirus-{current_checker}.html"
        r = requests.get(current_url)
        src = r.content
        soup = BeautifulSoup(src)
        elems = soup.find_all('div', class_="entry")
        if len(elems) > 0:
            current_date = soup.find_all('span', class_="stand")
            current_date = re.search(r"\d{2}(\.|-)\d{2}(\.|-)\d{4}",str(current_date)).group()
            urls.append(current_url)
            current_dates.append(current_date)
    print("--- gathered urls for pattern https://www.tagesschau.de/newsticker/liveblog-coronavirus-<somenumber>.html")
    for i in range(100,199,1):
        current_checker = str(i)
        current_url = f"https://www.tagesschau.de/newsticker/liveblog-corona-{current_checker}.html"
        r = requests.get(current_url)
        src = r.content
        soup = BeautifulSoup(src)
        elems = soup.find_all('div', class_="entry")
        if len(elems) > 0:
            current_date = soup.find_all('span', class_="stand")
            current_date = re.search(r"\d{2}(\.|-)\d{2}(\.|-)\d{4}",str(current_date)).group()
            urls.append(current_url)
            current_dates.append(current_date)
    print("--- gathered urls for pattern https://www.tagesschau.de/newsticker/liveblog-corona-<somenumber>.html")
    for i in range(100,199,1):
        for weekend_day in weekend_days:
            current_checker = str(i)
            current_url = f"https://www.tagesschau.de/newsticker/liveblog-corona-{weekend_day}-{current_checker}.html"
            r = requests.get(current_url)
            src = r.content
            soup = BeautifulSoup(src)
            elems = soup.find_all('div', class_="entry")
            if len(elems) > 0:
                current_date = soup.find_all('span', class_="stand")
                current_date = re.search(r"\d{2}(\.|-)\d{2}(\.|-)\d{4}",str(current_date)).group()
                urls.append(current_url)
                current_dates.append(current_date)
    print("--- gathered urls for pattern https://www.tagesschau.de/newsticker/liveblog-corona-<weekday>-<somenumber>.html")
    for i in range(100,199,1):
        for weekend_day in weekend_days:
            current_checker = str(i)
            current_url = f"https://www.tagesschau.de/newsticker/liveblog-coronavirus-{weekend_day}-{current_checker}.html"
            r = requests.get(current_url)
            src = r.content
            soup = BeautifulSoup(src)
            elems = soup.find_all('div', class_="entry")
            if len(elems) > 0:
                current_date = soup.find_all('span', class_="stand")
                current_date = re.search(r"\d{2}(\.|-)\d{2}(\.|-)\d{4}",str(current_date)).group()
                urls.append(current_url)
                current_dates.append(current_date)
    print("--- gathered urls for pattern https://www.tagesschau.de/newsticker/liveblog-coronavirus-<weekday>-<somenumber>.html")
    
    print("--- gathered all active urls ---") 
    print(f"--- extracted {len(urls)} urls and {len(current_dates)} corresponding dates")
    return urls, current_dates


def get_news(url):
    print("--- starting to gather entries ---")
    ## if you want to run this with selenium in container or use the accompanying docker-compose: docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:3.141.59-20200326
    browser = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
            )
    if browser:
        print("--- connection to selenium seems to work ---")
    else:
        print("--- connection to selenium seems not to work, for a remote connection spawn a container like so: docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:3.141.59-20200326 ---")

    ## running local with chromedriver.exe on path
    #browser = webdriver.Chrome()

    browser.get(url)
    time.sleep(1)

    elem = browser.find_element_by_tag_name("body")

    no_of_pagedowns = 100

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.15)
        no_of_pagedowns-=1

    post_elems = browser.find_elements_by_class_name("entry")
    titles = []
    dates = []
    contents = []
    for post in post_elems:
        post = post.text.split("\n")
        try:
            title = post[0]
        except:
            title = "empty"
        try:
            date = post[1]
        except:
            date = "empty"
        try:
            content = post[2]
        except:
            content = "empty"
        titles.append(title)
        dates.append(date)
        contents.append(content)
    print("--- gathered all loaded entries content ---") 
    return titles, dates, contents, url

def fetch_meta_create_df(titles, dates, contents, url, current_date):
    authenticator = IAMAuthenticator('NQntjlNUfMEKASwXHQY32rB9BPjEE7-gbBAEE0mWGPcv')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')
    
    organizations = []
    locations = []
    persons = []
    extraction_date = []
    news_url = []
    for i in range(len(contents)):
        response = natural_language_understanding.analyze(text=contents[i], language="de", features=Features(entities=EntitiesOptions(sentiment=False,limit=15))).get_result()
        organization = ""
        location = ""
        person = ""
        for item in response["entities"]:
            if item["type"] == "Organization":
                organization += item["text"] + " "
            if item["type"] == "Location":
                location += item["text"] + " "
            if item["type"] == "Person":
                person += item["text"] + " "
        organizations.append(organization)
        locations.append(location)
        persons.append(person)
        extraction_date.append(datetime.now().strftime('%Y-%m-%d'))
        news_url.append(url)
        
    datetimes = []
    for date in dates:
        try:
            dt_temp = datetime.strptime(date[:-4], '%d.%m.%Y %H:%M')
        except:
            dt_temp = datetime.strptime(current_date, '%d.%m.%Y')
        datetimes.append(dt_temp)
    
    #list(map(list, zip(*l)))
    
    table_columns = [datetimes, titles, contents, locations, organizations, persons, extraction_date, news_url]

    #df = pd.DataFrame(list(zip(datetimes, titles, contents, locations, organizations, persons, extraction_date, news_url)), 
    #           columns =['date','title', 'content', 'locations', 'organizations', 'persons', 'extraction_date', 'news_url']).iloc[1:,:]
    print("--- constructed the columns ---") 
    return table_columns



def write_to_db(table_columns, dbparams):

    dbname = dbparams.get('DB_DATABASE')
    dbuser = dbparams.get('DB_USER')
    dbpassword = dbparams.get('DB_PASSWORD')
    dbhost = dbparams.get('DB_HOST')
    dbport = dbparams.get('DB_PORT')

    tuples = tuple(map(tuple, zip(*table_columns)))

    conn = None
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, port=dbport, password=dbpassword)

        cur = conn.cursor()

        count = len(tuples)
        query = """
            INSERT INTO corona_events_tagesschau (publish_date, title, content, locations, organizations, persons, extraction_date, news_url)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s);
            """

        psycopg2.extras.execute_batch(cur,query,tuples)

        print(f"--- {count} rows inserted into the postgreDB executed ----")

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()


def run_scraper(url, current_date):
    titles, dates, contents, url = get_news(url)
    active_df = fetch_meta_create_df(titles, dates, contents, url, current_date)
    write_to_db(active_df)



def run_all(dbparams):
    print("--- starting the webscraper script ---")
    already_scraped_urls = check_scraped_urls(dbparams) 
    urls, current_dates = get_active_urls()
    i = 0
    untouched_urls = []
    corresp_dates = []
    for url, current_date in zip(urls, current_dates):
        if url not in already_scraped_urls:
            untouched_urls.append(url)
            corresp_dates.append(current_date)
        else:
            pass
    
    print(f" --- moving on with {len(untouched_urls)} new urls")

    for url, current_date in zip(untouched_urls, corresp_dates):
        i += 1
        print(f"||| start with the {i}. url |||")
        if current_date == datetime.now().strftime('%d.%m.%Y'):
            print(f"Let's wait till tomorrow to scrape {url} because its todays liveblog {current_date}")
        else: 
            print(f"lets scrape {url} with {current_date}")
            run_scraper(url, current_date)
        print(f"||| finished with the {i}. url |||")
    print("--- all set and done ---")

if __name__ == '__main__':
    my_dbparams_file=sys.argv[1]
    with open(my_dbparams_file) as json_file:
        dbparams = json.load(json_file)
    run_all(dbparams)

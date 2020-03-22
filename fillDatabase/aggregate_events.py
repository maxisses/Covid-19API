import psycopg2
from datetime import datetime
import WebScraping

def download_data():
    rows = WebScraping.scrape_something()
    write_to_db(rows)

def write_to_db(rows):
    try:
        conn = psycopg2.connect("dbname='wirvsvirus' user='wirvsvirus' host='marc-book.de' password='[n2^3kKCyxUGgzuV'")

        cur = conn.cursor()

        for item in rows:
            query = """
                INSERT INTO corona_events (extraction_date, referred_date, event_description, event_location, organisation)
                    VALUES
                    (%(extraction_date)s, %(referred_date)s, %(description)s, %(location)s, %(organisation)s)
                """
            content = {
                "extraction_date": item[0],
                "referred_date": item[1],
                "description": item[2],
                "location": item[3],
                "organisation": item[4],     
            }
            cur.execute(query, content)

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    download_data()

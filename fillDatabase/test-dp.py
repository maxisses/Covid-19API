import psycopg2
import requests

def downloadData():
    offsets = [0, 2000, 4000, 6000, 8000] #@TODO as long as result > 0

    for offset in offsets:
        url = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?f=json&where=1%3D1&outFields=*&resultOffset='+str(offset)
        r = requests.get(url, allow_redirects=True)
        json_tmp = r.json()
        #open("rki_data/" + str(offset) +'-rki.json', 'wb').write(json_tmp)
        writeToTable(json_tmp["features"])


def writeToTable(content):
    try:
        conn = psycopg2.connect("host= dbname=wirvsvirus user=wirvsvirus password=")

        cur = conn.cursor()

        cur.execute("""
            INSERT INTO rki_data_germany (state_id, state, sex, province_id, province, object_id, notification_date, death_count, case_count, age_group_start, age_group_end, extraction_date)
                VALUES
                (1, 'Bayern', 'M', 3, 'bla', 123, date'2020-01-01', 1, 12, 20, 30, date'2020-03-21')
        """)

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    downloadData()
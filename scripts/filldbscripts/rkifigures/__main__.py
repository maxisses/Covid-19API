import psycopg2
import psycopg2.extras
import requests
from datetime import datetime
import re

page_size = 2000
aggregation_frequency_max = 50
#offsets = [0,2000,4000,6000,8000,10000]

def download_data(dbparams):
    print(" Download data from https://services7.arcgis.com and writes them to the DB ")
    print("Let's start ...")
    i = 0
    entire_load = []
    while i < aggregation_frequency_max:
    #for offset in offsets:
        offset = i * page_size
        url = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?f' \
              '=json&where=1%3D1&outFields=*&resultOffset=' + str(offset)
        r = requests.get(url, allow_redirects=True)
        json_tmp = r.json()
        # open("rki_data/" + str(offset) +'-rki.json', 'wb').write(json_tmp)
        cleaned_columns = cleanup_data(json_tmp["features"])
        if len(cleaned_columns) is 0:
            break
        entire_load += cleaned_columns
        i += 1
    write_to_table(entire_load, dbparams)

def cleanup_data(json_files):
    result = []
    for attributes in json_files:
        # parse age group
        if attributes["attributes"]["Altersgruppe"] == 'unbekannt':
            age_group_start = '10000'
            age_group_end = '10000'
        elif attributes["attributes"]["Altersgruppe"] == 'A80+':
            age_group_start = '80'
            age_group_end = '99'
        else:
            age_group = re.search('A([0-9]*)-A([0-9]*)', attributes["attributes"]["Altersgruppe"], re.IGNORECASE)
            age_group_start = age_group.group(1)
            age_group_end = age_group.group(2)
            
        # parse notification_date
        ts = int(int(attributes["attributes"]["Meldedatum"]) / 1000)
        notification_date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        extraction_date = datetime.now().strftime('%Y-%m-%d')

        item = (
            parse_int(attributes["attributes"]["IdBundesland"]),
            attributes["attributes"]["Bundesland"],
            attributes["attributes"]["Geschlecht"],
            parse_int(attributes["attributes"]["IdLandkreis"]),
            attributes["attributes"]["Landkreis"],
            int(attributes["attributes"]["ObjectId"]),
            notification_date,
            int(attributes["attributes"]["AnzahlTodesfall"]),
            int(attributes["attributes"]["AnzahlFall"]),
            age_group_start,
            age_group_end,
            extraction_date 
        )

        result.append(item)
    return result

def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return -1


def write_to_table(content, dbparams):

    dbname = dbparams.get('DB_DATABASE')
    dbuser = dbparams.get('DB_USER')
    dbpassword = dbparams.get('DB_PASSWORD')
    dbhost = dbparams.get('DB_HOST')
    dbport = dbparams.get('DB_PORT')
    
    #print(f"sample record: {content[0]}")
    conn = None
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, port=dbport, password=dbpassword)

        print("________________________")
        print(f"--- connection to {dbname} established ---")
        print("________________________")

        cur = conn.cursor()

        count = len(content)
        query = """
            INSERT INTO rki_data_germany_refresh (state_id, state, sex, province_id, province, object_id, notification_date, death_count, case_count, age_group_start, age_group_end, extraction_date)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

        psycopg2.extras.execute_batch(cur,query,content)

        print("________________________")
        print(f"--- {count} queries executed and written to table rki_data_germany_refresh ----")
        print("________________________")

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def main(args):
    download_data(args)
    return {"done": 200}
import psycopg2
import requests
from datetime import datetime
import re

page_size = 2000
aggregation_frequency_max = 100
offsets = [0,2000,4000,6000,8000,10000]

def download_data():
    """Downloads data from https://services7.arcgis.com and writes them to the DB """
    print("Let's start ...")
    i = 0
    #while i < aggregation_frequency_max:
    for offset in offsets:
        #offset = i * page_size
        url = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?f' \
              '=json&where=1%3D1&outFields=*&resultOffset=' + str(offset)
        r = requests.get(url, allow_redirects=True)
        json_tmp = r.json()
        # open("rki_data/" + str(offset) +'-rki.json', 'wb').write(json_tmp)
        cleaned_columns = cleanup_data(json_tmp["features"])
        if len(cleaned_columns) is 0:
            break
        write_to_table(cleaned_columns)
        #i += 1

def cleanup_data(json_files):
    result = []
    for attributes in json_files:
        # parse age group
        if attributes["attributes"]["Altersgruppe"] == 'unbekannt':
            age_group_start = 'null'
            age_group_end = 'null'
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

        item = {
            'state_id': parse_int(attributes["attributes"]["IdBundesland"]),
            'state': attributes["attributes"]["Bundesland"],
            'sex': attributes["attributes"]["Geschlecht"],
            'province_id': parse_int(attributes["attributes"]["IdLandkreis"]),
            'province': attributes["attributes"]["Landkreis"],
            'object_id': int(attributes["attributes"]["ObjectId"]),
            'notification_date': notification_date,
            'death_count': int(attributes["attributes"]["AnzahlTodesfall"]),
            'case_count': int(attributes["attributes"]["AnzahlFall"]),
            'age_group_start': age_group_start,
            'age_group_end': age_group_end
        }

        if item["state"] == '-nicht erhoben-':
            item["state"] = ""

        if item["province"] == '-nicht erhoben-':
            item["province"] = ""

        result.append(item)
    return result

def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return -1


def write_to_table(content):

    dbname="ibmclouddb"
    dbuser="ibm_cloud_8dc51063_14dd_434a_a384_7964489602c3"
    dbpassword="a056050827df14622c64a1f1ff4f8e28932202c47635b4a55eaed0f6ca65c01e"
    dbhost="0a1fc5de-f2f9-42d8-bb7d-ddda460f96a5.bpb68u2f0gvaqgd0n64g.databases.appdomain.cloud"
    dbport="31790"

    conn = None
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, port=dbport, password=dbpassword)

        cur = conn.cursor()

        for idx, item in enumerate(content):
            query = """
                INSERT INTO rki_data_germany8 (state_id, state, sex, province_id, province, object_id, notification_date, death_count, case_count, age_group_start, age_group_end, extraction_date)
                    VALUES
                    ({}, '{}', '{}', {}, '{}', {}, date'{}', {}, {}, {}, {}, now())
                """.format(
                item['state_id'],
                item['state'],
                item['sex'],
                item['province_id'],
                item['province'],
                item['object_id'],
                item['notification_date'],
                item['death_count'],
                item['case_count'],
                item['age_group_start'],
                item['age_group_end']
            )

            cur.execute(query)
            print("--- query executed ----")

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def main(args):
    download_data()
    return {"done": 200}

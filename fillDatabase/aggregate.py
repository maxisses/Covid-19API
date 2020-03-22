#!/usr/bin/env python3
import psycopg2
import requests
from datetime import datetime
import re

page_size = 2000
aggregation_frequency_max = 100


def download_data():
    """Downloads data from https://services7.arcgis.com and writes them to the DB """
    print("Let's start ...")
    i = 0
    while i < aggregation_frequency_max:
        offset = i * page_size
        url = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?f' \
              '=json&where=1%3D1&outFields=*&resultOffset=' + str(offset)
        r = requests.get(url, allow_redirects=True)
        json_tmp = r.json()
        # open("rki_data/" + str(offset) +'-rki.json', 'wb').write(json_tmp)
        cleaned_columns = cleanup_data(json_tmp["features"])
        if len(cleaned_columns) is 0:
            break
        write_to_table(cleaned_columns)
        i += 1


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
    conn = None
    try:
        conn = psycopg2.connect("dbname='wirvsvirus' user='wirvsvirus' host='marc-book.de' password='[n2^3kKCyxUGgzuV'")

        cur = conn.cursor()

        for item in content:
            query = """
                INSERT INTO rki_data_germany (state_id, state, sex, province_id, province, object_id, notification_date,
                death_count, case_count, age_group_start, age_group_end, extraction_date)
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

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    download_data()

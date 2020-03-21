import psycopg2
import requests
import datetime

def downloadData():
    offsets = [0, 2000, 4000, 6000, 8000] #@TODO as long as result > 0
    print("Lets start ...")
    for offset in offsets:
        url = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?f=json&where=1%3D1&outFields=*&resultOffset='+str(offset)
        r = requests.get(url, allow_redirects=True)
        json_tmp = r.json()
        #open("rki_data/" + str(offset) +'-rki.json', 'wb').write(json_tmp)
        json_files.append(json_tmp)
        cleanedColumns = cleanUpData(json_files)
        writeToTable(cleanedColumns)

def cleanUpData(json_files):
    all_case_objects = []
    for json_file in json_files:
        for item in json_file["features"]:
            all_case_objects.append(item["attributes"])

    state_id = []
    state = []
    gender = []
    province_id = []
    province = []
    object_id = []
    reported_date = []
    death_count = []
    case_count = []
    age_group_start = []
    age_group_end = []
    extraction_date = []

    for case in all_case_objects:
        state_id.append(case['IdBundesland'])
        state.append(case['Bundesland'])
        gender.append(case['Geschlecht'])
        province.append(case['Landkreis'])
        province_id.append(case['IdLandkreis'])
        object_id.append(case['ObjectId'])
        reported_date.append(case['Meldedatum'])
        death_count.append(case['AnzahlTodesfall'])
        case_count.append(case['AnzahlFall'])
        age_group_start.append(case['Altersgruppe'].split("-")[0][1:])
        try:
            age_group_end.append(case['Altersgruppe'].split("-")[1][1:])
        except:
            age_group_end.append(None)
        extraction_date = datetime.datetime.today()

    all_columns = [state_id,state, gender, province_id, province, object_id, reported_date, death_count, case_count, age_group_start, age_group_end, extraction_date ]
    
    return(all_columns)

def writeToTable(content):
    try:
        conn = psycopg2.connect("dbname='wirvsvirus' user='wirvsvirus' host='marc-book.de' password='[n2^3kKCyxUGgzuV'")

        cur = conn.cursor()

        cur.execute("""
            INSERT INTO rki_data_germany (state_id,state, gender, province_id, province, object_id, reported_date, death_count, case_count, age_group_start, age_group_end, extraction_date )
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (content)
        )

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    downloadData()
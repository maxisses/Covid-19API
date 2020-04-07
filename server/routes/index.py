from server import app
from flask import render_template
import os
from flask import Flask, redirect
from flask import jsonify
from flask import request
from datetime import datetime, timedelta
import psycopg2
import psycopg2.extras

def handle_extraction_date(date):
        if date:
            return date
        else:
            if int(datetime.utcnow().strftime('%H')) >= 7:
                date = datetime.utcnow().strftime('%Y-%m-%d')
                print("set extraction date to today: " + str(date))
                return date
            else:
                date = (datetime.utcnow()-timedelta(1)).strftime('%Y-%m-%d')
                print("set extraction date to today: " + str(date))
                return date

def connect_to_db():
    dbname = os.getenv('DB_DATABASE')
    dbuser = os.getenv('DB_USER')
    dbpassword = os.getenv('DB_PASSWORD')
    dbhost = os.getenv('DB_HOST')
    dbport = os.getenv('DB_PORT')

    #print(dbname, user, password, host)
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, port=dbport, password=dbpassword)
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("connection to db failed")

    return cur

@app.route('/')
def hello_world():
    return redirect('https://github.com/maxisses/Covid-19API')

# GET /get_total_infected
# (parameter = zeitraum, nation, bundesland, city, gender, agegroup ... )
@app.route("/get_totals")
def get_totals():
    state = request.args.get('state')
    province = request.args.get('province')
    sex = request.args.get('sex')
    age_group_start = request.args.get('age_group_start')

    try:
        age_group_start = int(age_group_start)
    except:
        pass
    age_group_end = request.args.get('age_group_end')

    try:
        age_group_end = int(age_group_end)
    except:
        pass

    extraction_date = request.args.get('extraction_date')
    
    extraction_date = handle_extraction_date(extraction_date)

    date_range = request.args.get('date_range')

    date_range_start = None
    date_range_end = None
    try:
        date_range = date_range.split(" ")
        print("date_range len: " + str(len(date_range)))
        print("fetching the diff between two dates: " + " ".join(date_range))      
        if len(date_range) > 1:
            date_range_start = date_range[0]
            date_range_end = (datetime.strptime(date_range[1], '%Y-%m-%d') - timedelta(1)).strftime('%Y-%m-%d')
            print("1 - daterangeend: "+ str(date_range_end))
        else:
            date_range_start = (datetime.strptime(date_range[0], '%Y-%m-%d') - timedelta(1)).strftime('%Y-%m-%d')
            date_range_end = (datetime.strptime(date_range[0], '%Y-%m-%d') - timedelta(1)).strftime('%Y-%m-%d')
            print(f"2 - daterangeend: {str(date_range_end)}")
    except:
        if extraction_date:
            date_range_end = extraction_date
        else:
            if int(datetime.utcnow().strftime('%H')) >= 7:
                date_range_end = datetime.utcnow().strftime('%Y-%m-%d')
                print("set date_range_end date to today: " + str(date_range_end))
            else:
                date_range_end = (datetime.utcnow()-timedelta(1)).strftime('%Y-%m-%d')
                print("set extraction date to today: " + str(date_range_end))

    cur = connect_to_db()

    selection = {"extraction_date": extraction_date,"state":state, "province":province, "sex": sex, 
                "age_group_start":age_group_start, "age_group_end": age_group_end}

    columns = []
    for key, value in selection.items():
        if value:
            columns.append(key)
    columns = ", ".join(columns)
    #print(columns)

    
    selection["date_range_start"] = date_range_start
    selection["date_range_end"] = date_range_end

    ### get the numbers for the end
    cur.execute(""" SELECT {} , sum(case_count) AS infected, sum(death_count) AS deceased
                    FROM rki_data_germany_refresh 
                        WHERE (extraction_date = %(extraction_date)s OR %(extraction_date)s IS NULL )
                        AND (state = %(state)s OR %(state)s IS NULL )
                        AND (province = %(province)s OR %(province)s IS NULL)
                        AND (sex = %(sex)s OR %(sex)s IS NULL)
                        AND (age_group_start >= %(age_group_start)s OR %(age_group_start)s IS NULL)
                        AND (age_group_end <= %(age_group_end)s OR %(age_group_end)s IS NULL)
                        AND ((notification_date <= %(date_range_end)s) OR %(date_range_end)s IS NULL)
                        GROUP BY {}""".format(columns, columns), 
                        selection)

    rows_end = cur.fetchall()

    cur.execute(""" SELECT {} , sum(case_count) AS infected_in_range, sum(death_count) AS deceased_in_range
                    FROM rki_data_germany_refresh 
                        WHERE (extraction_date = %(extraction_date)s OR %(extraction_date)s IS NULL )
                        AND (state = %(state)s OR %(state)s IS NULL )
                        AND (province = %(province)s OR %(province)s IS NULL)
                        AND (sex = %(sex)s OR %(sex)s IS NULL)
                        AND (age_group_start >= %(age_group_start)s OR %(age_group_start)s IS NULL)
                        AND (age_group_end <= %(age_group_end)s OR %(age_group_end)s IS NULL)
                        AND ((notification_date BETWEEN %(date_range_start)s AND %(date_range_end)s) OR %(date_range_start)s IS NULL)
                        GROUP BY {}""".format(columns, columns), 
                        selection)

    rows = cur.fetchall()

    if len(rows) == 0:
        return jsonify({"message": "error or no values"}), 404
    else:
        if date_range_end:
            #print(rows_end[0]["infected"])
            rows[0]["total_infected"] =  rows_end[0]["infected"]
            rows[0]["total_deceased"] =  rows_end[0]["deceased"]
            try:
                rows[0]["from"] = (datetime.strptime(date_range_start, '%Y-%m-%d') + timedelta(1)).strftime('%Y-%m-%d')
                rows[0]["to"] = (datetime.strptime(date_range_end, '%Y-%m-%d') + timedelta(1)).strftime('%Y-%m-%d')
            except:
                rows[0]["from"] = None
                rows[0]["to"] = date_range_end
            rows[0]["meta"] = {
                "source URL(paginated)": "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?f=json&where=1%3D1&outFields=*&resultOffset=0",
                "source": "RKI Germany",
                "origin": "WirVsVirusHackathon - find the Team here: https://devpost.com/software/covid-19-api",
                "reference": "https://github.com/maxisses/Covid-19API",
                "maintainer": "Max Dargatz <max_dargatz@hotmail.com>"
            }
        
        return jsonify(rows[0])

# GET /get_data
@app.route("/get_data")
def get_data():
    state = request.args.get('state')
    province = request.args.get('province')
    sex = request.args.get('sex')
    age_group_start = request.args.get('age_group_start')

    try:
        age_group_start = int(age_group_start)
    except:
        pass
    age_group_end = request.args.get('age_group_end')

    try:
        age_group_end = int(age_group_end)
    except:
        pass
    extraction_date = request.args.get('extraction_date')

    extraction_date = handle_extraction_date(extraction_date)

    date_range = request.args.get('date_range')

    date_range_start = None
    date_range_end = None
    try:
        date_range = date_range.split(" ")
        if len(date_range) > 1:
            date_range_start = date_range[0]
            date_range_end = date_range[1]
        else:
            date_range_start = date_range[0]
            date_range_end = date_range[0]
    except:
        pass

    cur = connect_to_db()

    selection = {"extraction_date": extraction_date,"state":state, "province":province, "sex": sex, 
                "age_group_start":age_group_start, "age_group_end": age_group_end}

    columns = []
    for key, value in selection.items():
        columns.append(key)
    columns = ", ".join(columns)
    print(columns)
    
    selection["date_range_start"] = date_range_start
    selection["date_range_end"] = date_range_end

    print(selection)
    cur.execute(""" SELECT {} ,notification_date AS reported, case_count AS infected, death_count AS deceased
                    FROM rki_data_germany_refresh
                        WHERE (extraction_date = %(extraction_date)s OR %(extraction_date)s IS NULL )
                        AND (state = %(state)s OR %(state)s IS NULL )
                        AND (province = %(province)s OR %(province)s IS NULL)
                        AND (sex = %(sex)s OR %(sex)s IS NULL)
                        AND (age_group_start >= %(age_group_start)s OR %(age_group_start)s IS NULL)
                        AND (age_group_end <= %(age_group_end)s OR %(age_group_end)s IS NULL)
                        AND ((notification_date BETWEEN %(date_range_start)s AND %(date_range_end)s) OR %(date_range_start)s IS NULL)
                        """.format(columns, columns), 
                        selection)

    rows = cur.fetchall()

    if len(rows) == 0:
        return jsonify({"message": "error or no values"}), 404
    else:
        if date_range_start:
            for row in rows:
                row["from"] = date_range_start
                row["to"] = date_range_end
        return jsonify(rows)

# GET /get_events
@app.route("/get_events")
def get_events():
    locations = request.args.get('location')
    title = request.args.get('title')
    content = request.args.get('content')
    persons = request.args.get('person')
    organizations = request.args.get('organization')
    date_range = request.args.get('date_range')
    extraction_date = request.args.get('extraction_date')

    #extraction_date = handle_extraction_date(extraction_date)

    date_range_start = None
    date_range_end = None
    try:
        date_range = date_range.split(" ")
        print("fetching the diff between two dates: " + " ".join(date_range))
        if len(date_range) > 1:
            date_range_start = date_range[0]
            date_range_end = date_range[1]
        else:
            date_range_start = date_range[0]
            date_range_end = date_range[0]
    except:
        if extraction_date:
            date_range_end = extraction_date
        else:
            if int(datetime.utcnow().strftime('%H')) >= 7:
                date_range_end = datetime.utcnow().strftime('%Y-%m-%d')
                print("set date_range_end date to today: " + str(date_range_end))
            else:
                date_range_end = (datetime.utcnow()-timedelta(1)).strftime('%Y-%m-%d')
                print("set extraction date to today: " + str(date_range_end))

    cur = connect_to_db()
    
    ## to make the LIKE statement work this is neccessary
    if locations:
        locations = "%" + locations + "%"

    if organizations:
        organizations = "%" + organizations + "%"
    
    if persons:
        persons = "%" + persons + "%"
    
    if title:
        title = "%" + title + "%"

    if content:
        content = "%" + content + "%"
    

    selection = {"title": title, "content": content, "extraction_date": extraction_date,"locations":locations, "persons":persons, "organizations": organizations}

    columns = []
    for key, value in selection.items():
        columns.append(key)
    columns = ", ".join(columns)
    print(columns)

    selection["date_range_start"] = date_range_start
    selection["date_range_end"] = date_range_end

    print(selection)
    cur.execute(""" SELECT publish_date, title, content, locations, organizations, persons, extraction_date, news_url FROM corona_events_tagesschau
                        WHERE (extraction_date = %(extraction_date)s OR %(extraction_date)s IS NULL)
                        AND ((publish_date BETWEEN %(date_range_start)s AND %(date_range_end)s) OR %(date_range_start)s IS NULL)
                        AND (locations LIKE %(locations)s OR %(locations)s IS NULL)
                        AND (organizations LIKE %(organizations)s OR %(organizations)s IS NULL)
                        AND (persons LIKE %(persons)s OR %(persons)s IS NULL)
                        AND (title LIKE %(title)s OR %(title)s IS NULL)
                        AND (content LIKE %(content)s OR %(content)s IS NULL)
                        """, 
                        selection)

    rows = cur.fetchall()

    if len(rows) == 0:
        return jsonify({"message": "error or no values"}), 404
    else:
        if date_range_start:
            for row in rows:
                row["from"] = date_range_start
                row["to"] = date_range_end
        return jsonify(rows)

    #############################

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')

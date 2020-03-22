from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from datetime import datetime, timedelta
import psycopg2
import psycopg2.extras

app = Flask(__name__)

def create_app():
    """
    Create a Flask application using the app factory pattern.
    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__)

    cases = [
            {  
                "country": "Germany",
                "date": "19.03.2020",
                "lat": "51",
                "long": "9",
                "total_cases": 12000,
                "active_cases": 11000,
                "died_cases": 50
            },
            {  
                "country": "Germany",
                "date": "18.03.2020",
                "lat": "51",
                "long": "9",
                "total_cases": 11500,
                "active_cases": 11000,
                "died_cases": 30
            },
            {  
                "country": "France",
                "date": "19.03.2020",
                "lat": "46.2276",
                "long": "2.2137",
                "total_cases": 15000,
                "active_cases": 13000,
                "died_cases": 60
            }
        ]

    """ 
    mögliche Endpunkte der technischen Schnittstelle (API):

    Zahlen:

    get_cases (parameter = zeitraum, nation, bundesland, city, gender, agegroup ... )
    --> haben wir nich; get_recovered_per_day ( -,,-)
    --> haben wir nich; get_all_recoverd ( -,,-)
    get_active_cases ( -,,-)
    get_prediction ( -,,-)
    --> basierend auf Regression oder mehr

    Maßnahmen:

    get_political_measures (returns = datum, name, beschreibung, ... ) (parameter = Zeitraum, nation, ...)
    get_medical_measures (returns = name, beschreibung)
    --> im Kontext Ibuprofen eingeschränkt, in die Zukunft: impstoff gefunden, etc.
    """


    @app.route('/')
    def index():
        """
        Render our API documentation and some graphics here?
        """
        return render_template("index.html")

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
            print("fetching the diff between two dates: " + " ".join(date_range))
            if len(date_range) > 1:
                date_range_start = date_range[0]
                date_range_end = date_range[1]
            else:
                date_range_start = date_range[0]
                date_range_end = date_range[0]
        except:
            pass

        conn = psycopg2.connect("dbname='wirvsvirus' user='wirvsvirus' host='marc-book.de' password='[n2^3kKCyxUGgzuV'")
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        selection = {"extraction_date": extraction_date,"state":state, "province":province, "sex": sex, 
                    "age_group_start":age_group_start, "age_group_end": age_group_end}

        columns = []
        for key, value in selection.items():
            if value:
                columns.append(key)
        columns = ", ".join(columns)
        print(columns)

        
        selection["date_range_start"] = date_range_start
        selection["date_range_end"] = date_range_end

                ### get the numbers for the end
        cur.execute(""" SELECT {} , sum(case_count) AS infected, sum(death_count) AS deceased
                        FROM rki_data_germany 
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

        ### get the numbers for the start date
        cur.execute(""" SELECT {} , sum(case_count) AS infected, sum(death_count) AS deceased
                        FROM rki_data_germany 
                            WHERE (extraction_date = %(extraction_date)s OR %(extraction_date)s IS NULL )
                            AND (state = %(state)s OR %(state)s IS NULL )
                            AND (province = %(province)s OR %(province)s IS NULL)
                            AND (sex = %(sex)s OR %(sex)s IS NULL)
                            AND (age_group_start >= %(age_group_start)s OR %(age_group_start)s IS NULL)
                            AND (age_group_end <= %(age_group_end)s OR %(age_group_end)s IS NULL)
                            AND ((notification_date <= %(date_range_start)s) OR %(date_range_start)s IS NULL)
                            GROUP BY {}""".format(columns, columns), 
                            selection)

        rows_start = cur.fetchall()

        cur.execute(""" SELECT {} , sum(case_count) AS infected, sum(death_count) AS deceased
                        FROM rki_data_germany 
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
            return jsonify({"message": "error or no values"})
        else:
            if date_range_start:
                print(rows_end[0]["infected"])
                print(rows_start[0]["infected"])
                rows[0]["diff_infected"] =  rows_end[0]["infected"] - rows_start[0]["infected"]
                rows[0]["diff_deceased"] =  rows_end[0]["deceased"] - rows_start[0]["deceased"]
                rows[0]["from"] = date_range_start
                rows[0]["to"] = date_range_end
            return jsonify(rows)

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
            print(date_range)
            if len(date_range) > 1:
                date_range_start = date_range[0]
                date_range_end = date_range[1]
            else:
                date_range_start = date_range[0]
                date_range_end = date_range[0]
        except:
            pass

        

        conn = psycopg2.connect("dbname='wirvsvirus' user='wirvsvirus' host='marc-book.de' password='[n2^3kKCyxUGgzuV'")
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

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
                        FROM rki_data_germany 
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
            return jsonify({"message": "error or no values"})
        else:
            if date_range_start:
                for row in rows:
                    row["from"] = date_range_start
                    row["to"] = date_range_end
            return jsonify(rows)

    # GET /get_events
    @app.route("/get_events")
    def get_total_deceased():
        state = request.args.get('state')
        province = request.args.get('province')
        sex = request.args.get('type')
        age_group_start = request.args.get('description')
        extraction_date = request.args.get('extraction_date')
        date_range = request.args.get('date_range')

        date_range_start = None
        date_range_end = None
        try:
            date_range = date_range.split(" ")
            print(date_range)
            if len(date_range) > 1:
                date_range_start = date_range[0]
                date_range_end = date_range[1]
            else:
                date_range_start = date_range[0]
                date_range_end = date_range[0]
        except:
            pass

        return None


    #############################

    def handle_extraction_date(date):
        if date:
            return date
        else:
            #extraction_date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
            date = "2020-03-21"
            print("set extraction date to yesterday: " + str(date))
            return date
    
    return app

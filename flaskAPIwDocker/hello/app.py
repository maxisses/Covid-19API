from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
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

    # GET /get_total_cases
    # (parameter = zeitraum, nation, bundesland, city, gender, agegroup ... )
    @app.route("/get_total_cases")
    def get_total_cases():
        state = request.args.get('state')
        province = request.args.get('province')
        sex = request.args.get('sex')
        age_group_start = request.args.get('age_group_start')
        age_group_end = request.args.get('age_group_end')
        extraction_date = request.args.get('extraction_date')
        date_range = request.args.get('date_range')

        conn = psycopg2.connect("dbname='wirvsvirus' user='wirvsvirus' host='marc-book.de' password='[n2^3kKCyxUGgzuV'")
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        cur.execute("""SELECT state, province, sum(case_count) FROM rki_data_germany WHERE state=%s AND province=%s GROUP BY 1, 2""", [state, province])
        rows = cur.fetchall()

        if len(rows) == 0:
            return jsonify({"message": "error or no values"})
        else:
            return jsonify(rows)

    # GET /get_active_cases
    @app.route("/get_active_cases")
    def get_active_cases():
        country = request.args.get('country')
        response = []
        my_selection = filter(lambda x: x['country'] == country, cases)
        dict_filter= ["country", "date", "active_cases"]
        for el in my_selection:
            response.append({my_key: el[my_key] for my_key in dict_filter})

        if len(response) == 0:
            return jsonify(cases)
        else:
            return jsonify(response)

    # GET /get_died_cases
    @app.route("/get_died_cases")
    def get_died_cases():
        country = request.args.get('country')

        response = []
        my_selection = filter(lambda x: x['country'] == country, cases)
        dict_filter= ["country", "date", "died_cases"]
        for el in my_selection:
            response.append({my_key: el[my_key] for my_key in dict_filter})

        if len(response) == 0:
            return jsonify(cases)
        else:
            return jsonify(response)

    return app

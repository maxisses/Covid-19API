from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template


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

@app.route("/") # 'home'
def home():
    # return everything
    return render_template("index.html")

# GET /get_total_cases
@app.route("/get_total_cases")
def get_total_cases():
    country = request.args.get('country')
    response = []
    my_selection = filter(lambda x: x['country'] == country, cases)
    dict_filter= ["country", "date", "total_cases"]
    for el in my_selection:
        response.append({my_key: el[my_key] for my_key in dict_filter})

    if len(response) == 0:
        return jsonify(cases)
    else:
        return jsonify(response)

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

app.run(port=5000)

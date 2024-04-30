from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from map import trip, search_place, geocoding
import requests
import json

app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
app.secret_key = 'WBZiK?mS$SvA20D&0zMHJ5bYZu7a96'
app.config['SEARCH_HISTORY'] = []
api_key = "041c36486fc0b2772fd95e1912d43ef3"
# https://api.openweathermap.org/data/2.5/weather?lat=48.856613&lon=2.352222&appid=041c36486fc0b2772fd95e1912d43ef3

def get_weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if 'weather' in data and 'main' in data:
        description = data['weather'][0]['description']
        temperature_kelvin = data['main']['temp']
        temperature_celsius = temperature_kelvin - 273.15  # Convert temperature from Kelvin to Celsius
        return description, temperature_celsius
    else:
        return None, None


@app.route('/')
def index():
    # return render_template('index.html')
    search_history = session.get('search_history', app.config['SEARCH_HISTORY'])
    return render_template('index.html', history=search_history)


@app.route('/locate')
def locate():
    return render_template('search.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    if not query:
        return jsonify([])
    return jsonify(search_place(query))

@app.route('/info', methods=['POST'])
def info():
    value1 = request.form['searchInput']
    result = None

    if value1 != '':
        result = geocoding(value1, None)
        session['info_result'] = result
    return render_template(url_for('locate'))

@app.route('/submit', methods=['POST'])
def submit():
    value1 = request.form['input1']
    value2 = request.form['input2']
    mode = request.form['mode']
    result = None
    if value1 != '' and value2 != '' and mode != None:
        result, streetMap = trip(value1, value2, mode)
        
        # Add the search to the history
        app.config['SEARCH_HISTORY'].append({'origin': value1, 'destination': value2, 'mode': mode})
        session['search_history'] = app.config['SEARCH_HISTORY']
        
        # Fetch weather data for the origin coordinates
        if 'origin' in result:
            origin_lat, origin_lon = result['origin'][1], result['origin'][2]  # Extract latitude and longitude
            origin_weather, origin_temperature = get_weather(origin_lat, origin_lon, api_key)
        else:
            origin_weather, origin_temperature = None, None
        
        # Fetch weather data for the destination coordinates
        if 'destination' in result:
            destination_lat, destination_lon = result['destination'][1], result['destination'][2]  # Extract latitude and longitude
            destination_weather, destination_temperature = get_weather(destination_lat, destination_lon, api_key)
        else:
            destination_weather, destination_temperature = None, None
        
    return render_template('index.html', result=result, streetMap=streetMap, history=session.get('search_history', []),
                           origin_weather=origin_weather, origin_temperature=origin_temperature,
                           destination_weather=destination_weather, destination_temperature=destination_temperature)

def get_public_ip():
    try:
        # Make a request to the ipinfo.io API to get your public IP address
        response = requests.get('https://ipinfo.io/json')
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extract and return the public IP address
            return data['ip']
        else:
            print(f"Failed to retrieve public IP. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


@app.route('/myLocation', methods=['GET'])
def myLocation():
    KEY = "cfda6437ed9a8d"
    try:
        user_ip = get_public_ip()
        print(user_ip)
        
        url = f"https://ipinfo.io/{user_ip}?token={KEY}"
        print(url)
        response = requests.get(url)
        print(response);
        data = response.json()
        print(data)
        if 'city' in data:
            city = data['city'];
            print(city);
            return jsonify({'location': city})
        else:
            return jsonify({'error': 'City not found'})
    except Exception as e:
        print(f"Error in myLocation function: {e}")
        return jsonify({'error': 'An error occurred'})



    # KEY = "71a05ff63404ea7a184277bee7228e2f"

    #     url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={KEY}"
  



if __name__ == '__main__':
    app.run(debug=True)




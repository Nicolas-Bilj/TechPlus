from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from map import trip, search_place, geocoding
import json

app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
app.secret_key = 'WBZiK?mS$SvA20D&0zMHJ5bYZu7a96'
app.config['SEARCH_HISTORY'] = []

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
        
        # Ajouter la recherche à l'historique
        app.config['SEARCH_HISTORY'].append({'origin': value1, 'destination': value2, 'mode': mode})
        session['search_history'] = app.config['SEARCH_HISTORY']
    return render_template('index.html', result=result, streetMap=streetMap, history=session.get('search_history', []))

if __name__ == '__main__':
    app.run(debug=True)

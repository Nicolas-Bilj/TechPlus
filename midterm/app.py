from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from map import trip, search_place, geocoding

app = Flask(__name__)
app.secret_key = 'WBZiK?mS$SvA20D&0zMHJ5bYZu7a96'

@app.route('/')
def index():
    return render_template('index.html')

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
    return redirect(url_for('locate'))

@app.route('/submit', methods=['POST'])
def submit():
    value1 = request.form['input1']
    value2 = request.form['input2']
    mode = request.form['mode']
    result = None

    if value1 != '' and value2 != '' and mode != None:
        result = trip(value1, value2, mode)
        print(result)
        session['map_result'] = result
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

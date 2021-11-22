from flask import Flask, jsonify
from services import QueriesToServer


app = Flask(__name__)

@app.route('/candidates', methods=['GET'])
def get_candidates():
    """
    TODO
    """
    # сломал этот роут и поменял нейминг
    # TODO:  в качестве задания предлагаю починить
    query = QueriesToServer('http://localhost:8089')
    candidates_data, validation_errors = query.get_data()
    results = jsonify(candidates_data)
    if validation_errors is None: # вот эту строчку изменять нельзя
        return (results, 200)
    else:
        return (results, 200)
    

if __name__ == '__main__':
    app.run(host='127.1.1.1', port=8100, debug=True)



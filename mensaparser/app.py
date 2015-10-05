from flask import Flask, jsonify
from utils import get_api_as_json
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/api')
@app.route('/api/')
def api():
    return jsonify(get_api_as_json())


if __name__ == '__main__':
    app.debug = True
    app.run()

from flask import Flask, jsonify
from utils import get_api_as_json

app = Flask(__name__)


@app.route('/')
@app.route('/api')
def api():
    return jsonify(get_api_as_json())


if __name__ == '__main__':
    app.debug = True
    app.run()

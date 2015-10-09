import os.path, json, datetime
from flask import Flask, jsonify
from utils import get_api
from flask.ext.cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

api_content = ''


@app.route('/')
@app.route('/api')
@app.route('/api/')
def api():
    with open("api", "r") as myfile:
        data = myfile.read().replace('\n', '')

    data = json.loads(data)

    return jsonify(data)


@app.before_request
def write_file_to_system():
    if os.path.isfile('api'):
        print('file does exist')

        with open("api", "r") as myfile:
            data = myfile.read().replace('\n', '')

        data = json.loads(data)

        # check if file is old
        fromdate = data['date']
        fromdate = datetime.strptime(fromdate, "%Y-%m-%d %H:%M:%S.%f")
        fromdate = fromdate

        todate = datetime.now()

        fromhours = fromdate.timetuple()[3]
        tohours = todate.timetuple()[3]

        # check if outdated or  if outtimed (at 15 oclock the meal is resetted)
        if fromdate.date() < todate.date() or (fromhours < 15 <= tohours):
            # actualize
            print('actualize')
            actualize_api()

        else:
            pass

    else:
        print('file does not exists')
        actualize_api()


def actualize_api():
    # create file and fill with api
    with open("api", "w+") as f:
        data = json.dumps(get_api())
        f.write(data)


if __name__ == '__main__':
    app.run(debug=True)

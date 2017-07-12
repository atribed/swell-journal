from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

from model import BuoyReading

app = Flask(__name__)
app.config.from_envvar('SWELL_JOURNAL_CONFIG_PATH')

db = SQLAlchemy(app)


@app.route('/')
def home():
    date_begin = (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')
    date_end = datetime.today().strftime('%Y-%m-%d')
    return render_template('index.html', date_begin=date_begin, date_end=date_end)


@app.route('/buoy_info', methods=['GET'])
def get_buoy_info():
    buoy_id = request.values['buoy_id']
    date_start = request.values['date_s']
    date_end = request.values['date_e']
    readings = db.session.query(BuoyReading).filter(
        BuoyReading.buoy_id == buoy_id,
        BuoyReading.create_time >= date_start,
        BuoyReading.create_time <= date_end
    ).all()

    json_data = []
    for reading in readings:
        reading_data = {}
        reading_data['date'] = reading.create_time
        reading_data['swell_ht'] = reading.wave_data[0].swell_ht
        reading_data['swell_period'] = reading.wave_data[0].swell_period
        reading_data['wave_height'] = reading.wave_data[0].wave_height
        reading_data['wave_mean_period'] = reading.wave_data[0].wave_mean_period
        reading_data['wind_ht'] = reading.wave_data[0].wind_ht
        reading_data['wind_period'] = reading.wave_data[0].wind_period
        json_data.append(reading_data)

    return jsonify(json_data)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
                        help="run in debug mode (for use with PyCharm)", default=False)
    parser.add_argument("-p", "--port", dest="port",
                        help="port of server (default:%(default)s)", type=int, default=5001)

    cmd_args = parser.parse_args()
    app_options = {"port": cmd_args.port}

    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False

    app.run(**app_options)

import time
import atexit
import os
import math
import json
import datetime
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Blueprint, render_template
from scrapers import do_scrape_design_boom, do_scrape_design_milk

IS_PRODUCTION = os.environ.get('PYTHON_ENV') == 'PRODUCTION'
DEBUG = True if not IS_PRODUCTION else False
PORT = 5000 if not IS_PRODUCTION else os.environ.get('PORT')

app = Flask(__name__, static_url_path='', static_folder='build', template_folder='build')
static_folder = Blueprint('static', __name__, static_url_path='/api/static', static_folder='./static')
app.register_blueprint(static_folder)

scheduler = BackgroundScheduler()
atexit.register(lambda: stop_scheduler_if_running)



# --------------------------------------------------------------------------------
# UTILS
# --------------------------------------------------------------------------------

def stop_scheduler_if_running():
    try:
        scheduler.shutdown()
    except:
        pass

def do_thirty_minutes():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

def merge_static_json():
    path_to_json = 'static/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    result = []
    for file in json_files:
        with open(path_to_json+file) as f:
            data = json.load(f)
            result = result + data

    return json.dumps(result)


# --------------------------------------------------------------------------------
# ROUTES
# --------------------------------------------------------------------------------

@app.route('/data')
def data ():
    ''' GET - returns concatenated article data '''
    return merge_static_json()

@app.route('/')
def index ():
    ''' GET - returns "index.html" '''
    try:
        return render_template('index.html')
    except Exception as e:
        return "NO INDEX.HTML <br/> {}".format( str(e) )

# --------------------------------------------------------------------------------
# START THE APP
# --------------------------------------------------------------------------------

if __name__ == '__main__':
    print('::: {}'.format(PORT))

    scheduler.add_job(do_scrape_design_milk, 'cron', day_of_week='mon-fri', hour=1, minute=0)
    scheduler.add_job(do_scrape_design_boom, 'cron', day_of_week='mon-fri', hour=1, minute=15)
    scheduler.start()
    
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)


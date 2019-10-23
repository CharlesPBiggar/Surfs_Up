#Flask App for Hawaii Weather Data

#!! Steps to run file (Git-Windows): 1) python app.py 2) python -m flask run

#import dependencies
from flask import Flask

app = Flask(__name__)

#homepage route
@app.route('/')
def homepage():
    return 'This is the homepage!'

#precipitation page route
@app.route('/api/v1.0/precipitation')
def precipitation():
    return 'This page displays precipitation data'

#station page route
@app.route('/api/v1.0/stations')
def stations():
    return 'This page displays station data'

#
@app.route('/api/v1.0/tobs')
def tobs():
    return 'This page displays tobs data'


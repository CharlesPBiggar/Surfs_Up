#Flask App for Hawaii Weather Data

#!! Steps to run file (Git-Windows): 1) python app.py 2) python -m flask run

#import dependencies
from flask import Flask, jsonify
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#setup flask
app = Flask(__name__)

#setup SQLAlchemy and connection to db
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#set routes
#homepage route
@app.route('/')
@app.route('/home')
def homepage():
    return (f'Welcome to the Hawaii Weather App!<br/>'
            f'___________________________________<br/>'
            f'<br/>'
            f'List of Available Routes:<br/>'
            f'<br/>'
            f'1)For prescipitation data:<br/>'
            f'<br/>'
            f'/api/v1.0/precipitation<br/>'
            f'<br/>'
            f'2)For station data:<br/>'
            f'<br/>'
            f'/api/v1.0/station<br/>'
            f'<br/>'
            f'3)For Temperature Observations:<br/>'
            f'<br/>'
            f'/api/v1.0/tobs<br/>'
            f'<br/>'
            f'4) For a list of max, min and avg temperatures for a year upto specified date:<br/>'
            f'<br/>'
            f'/api/v1.0/<start><br/>' 
            f'<br/>'
            f'5) For a list of max, min and avg temperatures between user specified dates:<br/>'
            f'<br/>'
            f'/api/v1.0/<start>/<end><br/>'
            f'<br/>'
            f'6) If you need to return home:<br/>'
            f'<br/>'
            f'/home<br/>'
            f'___________________________________')

#precipitation page route
@app.route('/api/v1.0/precipitation')
def precipitation():
    last_year_start = (dt.date(2017,8,23) - dt.timedelta(days=365)).isoformat()
    query = (f'SELECT date, prcp FROM measurement \
                WHERE date > "{last_year_start}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'))

#station page route
@app.route('/api/v1.0/stations')
def stations():
    return 'This page displays station data'

#
@app.route('/api/v1.0/tobs')
def tobs():
    return 'This page displays tobs data'


if __name__ == "__main__":
    app.run(debug=True)
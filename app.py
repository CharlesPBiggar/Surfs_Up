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
            f'2)For stations data:<br/>'
            f'<br/>'
            f'/api/v1.0/stations<br/>'
            f'<br/>'
            f'3)For Temperature Observations:<br/>'
            f'<br/>'
            f'/api/v1.0/tobs<br/>'
            f'<br/>'
            f'4) For a list of max, min and avg temperatures for a year upto specified date:<br/>'
            f'<br/>'
            f'/api/v1.0/start<br/>'
            f'-- enter a date in the format YYYY-MM-DD where it says start above<br/>'
            f'-- ex:/api/v1.0/2017-01-01<br/>'
            f'<br/>'
            f'5) For a list of max, min and avg temperatures between user specified dates:<br/>'
            f'<br/>'
            f'/api/v1.0/start/end<br/>'
            f'-- enter a dates in the format YYYY-MM-DD where it says start & end above<br/>'
            f'-- ex:/api/v1.0/2017-01-01/2017-07-01<br/>'
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
    query = 'SELECT station, name FROM station'
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'))

#tobs page route
@app.route('/api/v1.0/tobs')
def tobs():
    sel = [Measurement.station, Measurement.id, Measurement.tobs]
    date = dt.datetime(2017, 8, 24)
    date2 = dt.datetime(2016, 8, 22)
    station4 = session.query(*sel).\
        filter(Measurement.station =="USC00519281").\
        filter(Measurement.date <= date).\
        filter(Measurement.date >= date2).\
        order_by(Measurement.date).all()
    station4
    return jsonify(station4)

#start date page route
@app.route('/api/v1.0/<start>')
def startdate(start = None):
   session = Session(engine)
   selection = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
   startdateres = session.query(*selection).\
       filter(Measurement.date >= start).all()
   result = list(np.ravel(startdateres))
   return jsonify(result)

#start/end date page route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    session = Session(engine)
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date
    
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

   
    results = session.query(*sel).\
        filter(Measurement.date >= start).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)
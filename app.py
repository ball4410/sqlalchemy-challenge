import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Import Flask
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Calculate the date one year from the last date in data set.
start_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (f"Homepage<br/>"
            f"<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start/end<br/>")


@app.route("/api/v1.0/precipitation")
def precip():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= start_date).all()
    
    session.close()
    
    
    precip_rows = {date: prcp for date, prcp in results}
    
    return jsonify(precip_rows)

@app.route("/api/v1.0/stations")
def station():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = session.query(Station.station).all()
    
    session.close()
    
    stations = list(np.ravel(results))
    
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').filter(Measurement.date >= start_date).all()
    
    session.close()
    
    tobs = list(np.ravel(results))
    
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start = None, end = None):
    #engine.execute("SELECT MIN(tobs), MAX(tobs), AVG(tobs) FROM measurement WHERE station = 'USC00519281'").fetchall()
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    select = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    if not end:
        results = session.query(*select).filter(Measurement.date >= start).all()
        
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*select).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
    
    temps = list(np.ravel(results))
    return jsonify(temps)
    

if __name__ == "__main__":
    app.run(debug=True)
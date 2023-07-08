# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
Measurement = base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Homepage!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Retrieve only the last 12 months of data to a dictionary 
    #using date as the key and prcp as the value.
    
    results=session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()
    

    session.close()
    
   #Return the JSON representation of your dictionary.
    all_prec = list(np.ravel(results))

    return jsonify(all_prec)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Return a JSON list of stations from the dataset.
    results=session.query(Measurement.station).all()
    
    session.close()
    
    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
    
    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Query the dates and temperature observations of 
    # the most-active station for the previous year of data.
   
    results=session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.station == 'USC00519281').all()
    
    session.close()

    #Return a JSON list of temperature observations for the previous year.
    all_temps = list(np.ravel(results))

    return jsonify(all_temps)


@app.route("/api/v1.0/<start>")
def temperature_range_start(start):
    """Return the minimum, average, and maximum temperature for a given start date"""
    session = Session(engine)
    temperature_stats = session.query(func.min(Measurement.tobs),
                                      func.avg(Measurement.tobs),
                                      func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    return jsonify(temperature_stats)

@app.route("/api/v1.0/<start>/<end>")
def temperature_range_start_end(start, end):
    """Return the minimum, average, and maximum temperature for a given start and end date range"""
    session = Session(engine)
    temperature_stats = session.query(func.min(Measurement.tobs),
                                      func.avg(Measurement.tobs),
                                      func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    return jsonify(temperature_stats)
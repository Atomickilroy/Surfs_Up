#Flask Weather Application


#Import dependencies for Flask Weather app
import datetime as dt
import numpy as np
import pandas as pd

#Dependencies for SQLAlchemy 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Lastly dependencies for Flask
from flask import Flask, jsonify

#Set up the database 
engine = create_engine('sqlite:///hawaii.sqlite')

# Reflect the database into our classes 'getting it ready'
Base = automap_base()

#Reflect the database
Base.prepare(engine, reflect = True)

#Save our references to variables 
Measurement = Base.classes.measurement
Station = Base.classes.station

#Finally Create a Link from py to our database
session = Session(engine)

#Define Flask app
app = Flask(__name__)

#9.5.2 Create the Welcome Route

#define the Welcome route ' this is considered our 'root''
@app.route("/")


#add routing information by first creating a function and return statement
#then using an f string add in the routes we'll need for this mod

def welcome():
    return(

    '''
    Welcome to the Climate Analysis API!

    Available Routes:

    /api/v1.0/precipitation

    /api/v1.0/stations

    /api/v1.0/tobs

    /api/v1.0/temp/start/end

    ''')

#Create Precipitation Route
@app.route("/api/v1.0/precipitation")

#Next create a function
def precipitation():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
      
    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)

#Create the Stations Route
#Looking to return a list of the stations

@app.route("/api/v1.0/stations")

#Define the stations function
def stations():

  results = session.query(Station.station).all()
  #query that will get all stations
  stations = list(np.ravel(results))
  #jsonify the list and return JSON
  return jsonify(stations=stations)

@app.route("/app/v1.0/tobs")

def temp_monthly():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))
    
    return jsonify(temps)

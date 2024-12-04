# Import the dependencies.
import datetime as dt
import numpy as np

from sqalchemy.ext.automap import automap_base
from sqalchemy.orm import session
from sqalchemy import creat_engine, func

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
measurement = base.classes.measurement
station = base.classes.station

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
    return (
        f"Hawaii Climate Analysis API<br/>"
        f"Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<start><br/>"
        f"/api/v1.0/temp/<start>/<end><br/>"

)

@app.route("/api/v1.0/precipitaton")
def precipitation():
    # Calculate the date one year from the last date in data set.

    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    precipitation = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= last_year).all()

    session.close()

    precip = {date:prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.station).all()

    session.close()
#unravel results into a 1D array, they are usually in a 2D array when using SQLAlchemy
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():

    most_active = session.query(measurement.station,\ 
    func.count(measurement.station)).\
group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()
    most_active_station = most_active[0]

    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(measurement.tobs).\
    filter(measurement.station == most_active_station).\
    filter(measurement.date >= last_year).all()

    session.close()

    temp = list(np.ravel(results))
    return jsonify(temp=temp)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(
    start = dt.date(2016,8,23)
    end = dt.date(2017,8,23)
):
    if not end:
        results = session.query(
            func.min(measurement.tobs),
            func.avg(measurement.tobs),
            func.max(measurement.tobs)
                ).filter(measurement.date >= start).all()

        session.close()

        stats = list(np.ravel(results))
        return jsonify(stats)

    results = session.query(
            func.min(measurement.tobs),
            func.avg(measurement.tobs),
            func.max(measurement.tobs)
                ).filter(measurement.date >= start).\
                filter(measurement.date<= end).all()
   
    session.close()

    stats = list(np.ravel(results))
    return jsonify(stats=stats)


if __name__ == "//main//":
    app.run()
   


    

















    
        

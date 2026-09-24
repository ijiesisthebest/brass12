"""Flask web application for browsing musical instruments and models."""

import sqlite3
from flask import Flask, g, render_template

# define path for database
DATABASE = 'database.db'

# initialise app
app = Flask(__name__)


def get_db():
    """Get the database connection."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(_exception):
    """Close the database connection."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """Run a database query and return the results."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    # Returns a single row if one is right
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def home():
    """Display the home page with all instruments."""
    # home page for instruments
    sql = """
          SELECT Instrument_ID, Name, Image
          FROM Instrument;
          """
    results = query_db(sql)
    return render_template("home.html", results=results)


@app.route("/instrument/<int:instrument_id>")
def instrument(instrument_id):
    """Display models belonging to an instrument."""
    sql = """
    SELECT
        Model.Model_ID,
        Brand.Brand_Name,
        Model.Model_name,
        Model.Price,
        Model.Image
    FROM Model
    JOIN Brand ON Brand.Brand_ID = Model.Brand_ID
    JOIN Instrument ON Instrument.Instrument_ID = Model.Instrument_ID
    WHERE Instrument.Instrument_ID = ?;
    """
    result = query_db(sql, (instrument_id,))

    if not result:
        return "Instrument does not exist"

    return render_template("instrument.html", results=result)


@app.route("/model/<int:model_id>")
def model(model_id):
    """Display details for a specific model."""
    sql = """
    SELECT
        Model.Model_ID,
        Instrument.Name,
        Brand.Brand_Name,
        Model.Model_name,
        Model.Price,
        Model.Image,
        Model.Description,
        Brand.Country
    FROM Model
    JOIN Brand
        ON Model.Brand_ID = Brand.Brand_ID
    JOIN Instrument
        ON Model.Instrument_ID = Instrument.Instrument_ID
    WHERE Model.Model_ID = ?;
    """
    result = query_db(sql, (model_id,), one=True)

    if result is None:
        return "Model does not exist"

    return render_template("model.html", result=result)


@app.route("/whybrass")
def whybrass():
    """Display the why brass page."""
    return render_template("whybrass.html")


@app.route("/care")
def care():
    """Display the instrument care page."""
    return render_template("care.html")


@app.route("/history")
def history():
    """Display the history page."""
    return render_template("history.html")


if __name__ == "__main__":
    app.run(debug=True)

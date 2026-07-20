from flask import Flask, g, render_template
import sqlite3

# define path for database
DATABASE = 'database.db'

# initialise app
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    # Returns a single row if one is right
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def home():
    # home page for instruments
    sql = """
          SELECT Instrument_ID, Name, Image
          FROM Instrument;
          """
    results = query_db(sql)
    return render_template("home.html", results=results)


@app.route("/instrument/<int:id>")
def instrument(id):
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
    result = query_db(sql, (id,))
    return render_template("instrument.html", results=result)


@app.route("/model/<int:id>")
def model(id):
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
    result = query_db(sql, (id,), one=True)
    return render_template("model.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)

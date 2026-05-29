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
    # just one instrument model based on id
    sql = """SELECT * FROM Model
    JOIN Brand ON Brand.Brand_ID = Model.Brand_ID
    JOIN Instrument ON Instrument.Instrument_ID = Model.Instrument_ID
    WHERE Model.Model_ID = ?;"""
    result = query_db(sql, (id,), True)
    return str(result)


if __name__ == "__main__":
    app.run(debug=True)

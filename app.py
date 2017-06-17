#cd 2017\DTP\Fox_II_Website
#c:\Python34\python.exe app.py

import sqlite3
from flask import Flask, render_template
app = Flask(__name__, template_folder="templates")

conn = sqlite3.connect('database/Fox_II.db')
print ("Opened database successfully") #Confirm database connection.
conn.close()

@app.route("/")
def index():
    con = sqlite3.connect("database/Fox_II.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from home")

    rows = cur.fetchall();    
    return render_template("index.html", rows = rows)

@app.route("/rates/")
def rates():
    return render_template("rates.html")

@app.route("/charter/")
def charter():
    return render_template("charter.html")

@app.route("/about_us/")
def about_us():
    return render_template("about_us.html")

@app.route("/faqs/")
def faqs():
    return render_template("faqs.html")

@app.route("/not_available")
def na():
    return render_template("not_available.html")

if __name__ == "__main__":
    app.run()
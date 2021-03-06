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
    cur.execute("select surname, firstname, country from customer cu, country co where cu.CountryCode = co.CountryCode")
     

    rows = cur.fetchall();    
    return render_template("index.html", rows = rows)

@app.route("/rates/")
def rates():
    con = sqlite3.connect("database/Fox_II.db")
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()
    cur.execute("select * from PNA where id='1'")
         
    
    rows = cur.fetchall();     
    return render_template("rates.html", rows = rows)

@app.route("/charter/")
def charter():
    con = sqlite3.connect("database/Fox_II.db")
    con.row_factory = sqlite3.Row
       
    cur = con.cursor()
    cur.execute("select * from PNA where id='2'")
            
       
    rows = cur.fetchall();     
    return render_template("charter.html", rows = rows)

@app.route("/about_us/")
def about_us():
    con = sqlite3.connect("database/Fox_II.db")
    con.row_factory = sqlite3.Row
           
    cur = con.cursor()
    cur.execute("select * from PNA where id='3'")
                
           
    rows = cur.fetchall();     
    return render_template("about_us.html", rows = rows)

@app.route("/faqs/")
def faqs():
    con = sqlite3.connect("database/Fox_II.db")
    con.row_factory = sqlite3.Row
              
    cur = con.cursor()
    cur.execute("select * from PNA where id='4'")
                   
              
    rows = cur.fetchall();     
    return render_template("faqs.html", rows = rows)

@app.route("/not_available")
def na():
    return render_template("not_available.html")

if __name__ == "__main__":
    app.run()
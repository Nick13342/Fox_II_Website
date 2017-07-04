#cd 2017\DTP\Fox_II_Website
#c:\Python34\python.exe app.py

import sqlite3
from customer import Customer
from flask import Flask, render_template, request
app = Flask(__name__, template_folder="templates")
global cust
global con

con = sqlite3.connect('database/Fox_II.db')
print ("Opened database successfully") #Confirm database connection.
#con.close()

@app.route("/")
def index():
    global con
    
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select contentH, question, contentFAQ from home, faq")
     

    rows = cur.fetchall();
    
    #----------------
    global cust
    cust = Customer()
    cust.readCust(con,2)
    print(cust.emailAddr)
    print(cust.dob)
    cust.emailAddr = 'test'
    if cust.updateCust(con, 2) == True:
        print("Updated")
    else:
        print("Failed")
    print(cust.surname)
    print(cust.emailAddr)
    #----------------
    
    return render_template("index.html", rows = rows)

@app.route("/rates/")
def rates():
    global cust
    global con
    
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()
    cur.execute("select * from PNA where id='1'")
         
    
    rows = cur.fetchall();
    
    cust.readCust(con,2)   
    print(cust.surname)
    print(cust.emailAddr)
    print(cust.dob)
    
    return render_template("rates.html", rows = rows)

@app.route("/charter/")
def charter():
    global con
    
    con.row_factory = sqlite3.Row
       
    cur = con.cursor()
    cur.execute("select * from PNA where id='2'")
            
       
    rows = cur.fetchall();     
    return render_template("charter.html", rows = rows)

@app.route("/bookings/")
def bookings():
    global con
        
    con.row_factory = sqlite3.Row
                  
    cur = con.cursor()
    cur.execute("select * from PNA where id='5'")
                       
                  
    rows = cur.fetchall();     
    return render_template("bookings.html", rows = rows)

@app.route("/about_us/")
def about_us():
    global con
    
    con.row_factory = sqlite3.Row
           
    cur = con.cursor()
    cur.execute("select * from PNA where id='3'")
                
           
    rows = cur.fetchall();     
    return render_template("about_us.html", rows = rows)

@app.route("/faqs/")
def faqs():
    global con
    
    con.row_factory = sqlite3.Row
              
    cur = con.cursor()
    cur.execute("select * from PNA where id='4'")
                   
              
    rows = cur.fetchall();     
    return render_template("faqs.html", rows = rows)

@app.route("/thisisasecretpage/admin/")
def admin():
    global con
        
    con.row_factory = sqlite3.Row
                  
    cur = con.cursor()
    cur.execute("select * from PNA where id='6'")
                       
                  
    rows = cur.fetchall();    
    return render_template("admin.html", rows = rows)

@app.route("/not_available")
def na():
    return render_template("not_available.html")

if __name__ == "__main__":
    app.run()
#cd 2017\DTP\Fox_II_Website
#c:\Python34\python.exe app2.py

import sqlite3
from customer import Customer
from schedule import Schedule
from flask import Flask, render_template, request
app = Flask(__name__, template_folder="templates")
global cust
global con
sched = Schedule()

con = sqlite3.connect('database/Fox_II.db')
#Makes sure foreign keys are enforced.
con.execute('pragma foreign_keys=ON')
print ("Opened database successfully") #Confirm database connection.
#con.close()

@app.route("/")
def index():
    global con
    sched = Schedule()
    
    startDate = '2017-10-16'
    endDate = '2017-10-17'
    (dbStatus, rows) = sched.readSchedulebyDate(con, startDate, endDate)
    
    return render_template("index.html", rows = rows)

@app.route("/rates/")
def rates():
    global cust
    global con
    
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()
    cur.execute("select * from PNA where id='1'")
         
    
    rows = cur.fetchall();
    
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
    sched = Schedule()
    
    startDate = '2017-01-01'
    endDate = '2017-12-31'
    Status = None
    (dbStatus, rows) = sched.readSchedulebyDate(con, startDate, endDate)
    
    if (dbStatus == True):
        return render_template("bookings.html", rows = rows)
    else:
        return render_template('not_available.html', error = sched.error)

@app.route("/singlebooking/", methods = ['POST'])
def singlebooking():
    global con
    sched = Schedule()
        
    if request.method == 'POST':
        CruiseDate = request.form['label'].split('.')[0]
        CruiseNo = int(request.form['label'].split('.')[1])
        
        
    (dbStatus, rows) = sched.readSched(con, CruiseDate, CruiseNo)
        
    return render_template("singlebooking.html", rows = rows)

@app.route("/custdetails/")
def custdetails():
    
    return render_template("custdetails.html")

@app.route("/schedules/")
def schedules():
    global con
    
    schedRows = None
    Status = None
    #Create new schedule object.
    sched = Schedule()
    #Return cruise schedules between dates.
    (Status, schedRows) = sched.readSchedulebyDate(con,"2017-10-16", "2017-10-17")
    if (Status == True):
        return render_template("schedule.html", rows = schedRows)
    else:
        return render_template('not_available.html', error = sched.error)

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

@app.route("/thisisaverysecretpage/admin/")
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
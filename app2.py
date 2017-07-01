#cd 2017\DTP\Fox_II_Website
#c:\Python34\python.exe app.py

import sqlite3
from flask import Flask, render_template
app = Flask(__name__, template_folder="templates")
global cust
global con

con = sqlite3.connect('database/Fox_II.db')
print ("Opened database successfully") #Confirm database connection.
#con.close()


class Customer:
    
    def __init__(self):
        self.__surname = ""
        self.__firstname = ""
        self.__email = ""
        
    def readCust(self,con,CustID):
        read_query = "select * from customer where CustID = ?"
        
        con.row_factory = sqlite3.Row
        
        cur = con.cursor()
        cur.execute(read_query, (CustID,))
        
        row = cur.fetchone();
        
        self.__surname = row['surname']
        self.__firstname = row['firstname']
        self.__email = row['email']
        
    @property
    def surname(self):
        return self.__surname

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
    print(cust.surname)
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
    
    print(cust.surname)
    
    return render_template("rates.html", rows = rows)

@app.route("/charter/")
def charter():
    global con
    
    con.row_factory = sqlite3.Row
       
    cur = con.cursor()
    cur.execute("select * from PNA where id='2'")
            
       
    rows = cur.fetchall();     
    return render_template("charter.html", rows = rows)

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

@app.route("/not_available")
def na():
    return render_template("not_available.html")

if __name__ == "__main__":
    app.run()
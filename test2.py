#cd 2017\DTP\Fox_II_Website
#c:\Python34\python.exe app.py

import sqlite3
from customer import Customer
from emailAddress import email
from schedule import Schedule
from datetime import datetime

global cust
global con


def validateDT(date_text, format):
    try:
        if date_text != datetime.strptime(date_text, format).strftime(format):
            raise ValueError
        return True
    except ValueError:
        return False
        

if validateDT("2017-12-12","%Y-%m-%d"):
    print("Date successful")
else:
    print("Date failed")


if validateDT("09:30","HH:MM"):
    print("Time successful")
else:
    print("Time failed")

exit()

# - email testing 
# emails = []
# 
# emails.append(email("brent@glanville@healthscope.co.nz"))
# emails.append(email("brent.glanville@healthscope.co.nz"))
# if emails[0].validEmailAddress():
#     print("Valid email address")
# else:    
#     print(emails[0].error)
# 
# if emails[1].validEmailAddress():
#     print("Valid email address")
# else:    
#     print(emails[1].error)

# --------Customer part ------    
con = sqlite3.connect('/Users/bglanv/Documents/Personal/bhs.db')
con.execute('pragma foreign_keys=ON')
#con = sqlite3.connect("database/Fo_II.db")
print ("Opened database successfully") #Confirm database connection.


# schedRows = None
# sched = Schedule()
# print("reading schedule")
# (dbStatus, schedRows) = sched.readSchedulebyDate(con,"2017-10-17", "2017-10-16")
# if (dbStatus == True):
#     for myRow in schedRows:
#         print(myRow["CruiseDate"])
#         print(myRow["CruiseNo"])
#         print(myRow["departure"])
#         print(myRow["name"])
# else:
#      print(sched.error)

# Create new customer
custRow = []
cust = Customer()

# Create new customer
print("Inserting Customer")
cust.surname = "Glanville"
cust.firstname = "Nick"
#cust.emailAddr = "abc@google.co.nz"
cust.emailAddr = ""
cust.gender = "F"
cust.countryCode = "NZL"
cust.phone = "0274345288"
cust.dob = "1999-12-03"
if cust.insertCust(con):
    print("Customer inserted OK")
else:
    print(cust.error)

# Reading Customer now returns rows
print("reading customer .....")
(dbStatus, custRow) = cust.readCust(con,2)
if (dbStatus == True):    
    print(cust.emailAddr)
    print(cust.dob)
    print(custRow["surname"])
else:
     print(cust.error)
     
# Reading Customer now returns rows
print("reading customer by email.....")
(dbStatus, custRow) = cust.readCustbyEmail(con,"qwerty")
if (dbStatus == True):    
    print(cust.emailAddr)
    print(cust.dob)
    print(custRow["surname"])
else:
     print(cust.error)     
# cust.emailAddr = 'test'
# if cust.updateCust(con, 2) == True:
#     print("Updated")
# else:
#     print("Failed!!!!")
# 
#  
#     
# print("reading customer back....")    
# cust.readCust(con,2)   
# print(cust.surname)
# print(cust.emailAddr)
# print(cust.dob)
# 
# con.close()
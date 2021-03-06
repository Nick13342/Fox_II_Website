#cd 2017\DTP\Fox_II_Website
#c:\Python34\python.exe app.py

import sqlite3
from customer import Customer
from emailAddress import Email
from schedule import Schedule
from booking import Booking
from country import Country
from datetime import datetime
from dateutil.relativedelta import relativedelta

global cust
global con


# def validateDT(date_text, format):
#     try:
#         if date_text != datetime.strptime(date_text, format).strftime(format):
#             raise ValueError
#         return True
#     except ValueError:
#         return False
#         
# 
# if validateDT("2017-12-12","%Y-%m-%d"):
#     print("Date successful")
# else:
#     print("Date failed")
# 
# 
# if validateDT("09:30","HH:MM"):
#     print("Time successful")
# else:
#     print("Time failed")
# 
# exit()

#- email testing 
# emails = []
# 
# emails.append(Email("brent@glanville@healthscope.co.nz"))
# emails.append(Email("b.g@gmail.co.nz"))
# if emails[0].validEmailAddress():
#     print("Valid email address")
# else:    
#     print(emails[0].error)
# 
# if emails[1].validEmailAddress():
#     print("Valid email address")
# else:    
#     print(emails[1].error)
# 
# exit()
# --------Customer part ------    
con = sqlite3.connect('/Users/bglanv/Documents/Python/Projects/FoxII/database/Fox_II.db')
con.execute('pragma foreign_keys=ON')
#con = sqlite3.connect("database/Fo_II.db")
print ("Opened database successfully") #Confirm database connection.


format = '%Y-%m-%d'
years_ago = datetime.now() - relativedelta(years=5)

print("Years Ago: ", years_ago.strftime(format))
exit()

# book = Booking()
# 
# book.CruiseDate = "2017-10-17"
# print('CruiseDate: ',book.CruiseDate)
# book.CruiseNo = 1
# book.CustID = 18
# book.adults = 1
# book.children = 2
# dbStatus = book.insertBooking(con)
# if (dbStatus == True):
#     print('Booking ID is: ',book.BookingID)
# else:
#     print(book.error)



# schedRows = None
# sched = Schedule()
# print("reading schedule")
# (dbStatus, schedRows) = sched.readSched(con,"2017-10-16", 2)
# #(dbStatus, schedRows) = sched.readSchedulebyDate(con,"2017-10-16", "2017-10-17")
# if (dbStatus == True):
#     for myRow in schedRows:
#         print(myRow["CruiseDate"])
#         print(myRow["CruiseNo"])
#         print(myRow["departure"])
#         print(myRow["name"])
# else:
#     print(sched.error)

#exit()
# cntry = Country()
# (dbStatus, name) = cntry.readCountryByCode(con,'nzl')
# print ('CountryName: ',name)


# Create new customer
custRow = []
cust = Customer(con,'NZL')
print('Customer country code: ', cust.countryCode)


#(dbStatus, custRow) = cust.readCustbyEmail(con,"blah@xtra.co.nz")
# (dbStatus, custRow) = cust.readCustbyEmail(con,"abc@gmail.com")
# if (dbStatus == True):
#     print(cust.surname)
# else:
#      print(cust.error)     
# cust.surname = ""
# dbStatus = cust.updateCust(con,cust.CustID)
# if dbStatus == True:
#     print('Updated Successfully')
# else:
#     print('Error:', cust.error)
# 
# exit()

# Create new customer
print("Inserting Customer")
cust.surname = "Glanville"
cust.firstname = "Nick"
cust.emailAddr = "xyz@google.com"
#cust.emailAddr = ""
cust.gender = "F"
cust.countryCode = "NZL"
cust.phone = "0274345288"
cust.dob = "1999-12-03"
if cust.insertCust(con):
    print("Customer inserted OK")
else:
    print(cust.error)
exit()

# # Reading Customer now returns rows
# print("reading customer .....")
(dbStatus, custRow) = cust.readCust(con,2)
if (dbStatus == True):
    print(cust.emailAddr)
    print(cust.dob)
#    print(custRow["surname"])
else:
      print(cust.error)

cust.newBooking()
cust.emailAddr = 'test'
if cust.updateCust(con, 2) == True:
    print("Updated")
else:
    print("cust.error")
# Reading Customer now returns rows
# print("reading customer by email.....")
# (dbStatus, custRow) = cust.readCustbyEmail(con,"blah@xtra.co.nz")
# if (dbStatus == True):
#     print(cust.error)
#     print(cust.emailAddr)
#     print(cust.surname)
# #    print(custRow["surname"])
# else:
#      print(cust.error)     
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
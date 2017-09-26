#cd 2017\DTP\Fox_II_Website
#c:\Python34\python.exe app2.py
#"F:\Program Files (x86)\Python\Python36-32\python.exe" app2.py

# Import standard Python modules
import sqlite3
from flask import Flask, render_template, request, session
app = Flask(__name__, template_folder="templates")
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Import custom modules here.
from customer import Customer
from schedule import Schedule
from booking import Booking
from emailAddress import Email
from country import Country
from route import Route
from boat import Boat
from admin import Login
from debug import Debug


# require a secret key for session data to work OK.  Just needs
# to be a random 20 characters
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

# set a global varibale to allow database connection to be used
# throughout the program
global con

#---------------------------------------------------------------------------
# Create a debug object here.  Either set to True for debugging or False
# Set to False by default and we can enable / disable it when we like
#---------------------------------------------------------------------------
db = Debug("app2", True)


#---------------------------------------------------------------------------
# Make a connection to the database
#---------------------------------------------------------------------------
con = sqlite3.connect('database/Fox_II.db')
#Makes sure foreign keys are enforce for database integrity
con.execute('pragma foreign_keys=ON')

#Confirm database connection.
db.print ("Opened database successfully") 


#----------------------------------------------------------------------------
# Procedure to read the Country table and populate the list before
# rendering in the customer details page
#----------------------------------------------------------------------------
def readCountryTable():
    #create country object and read the Countries
    ctry = Country()
    (dbStatus, countries)  = ctry.readCountries(con)
    if (dbStatus == False):
        return render_template('error.html', error = ctry.error)
    else:
        return(countries)
 
#----------------------------------------------------------------------------
# Procedure to read the Boat table and populate the list before
# rendering in the schedule details page
#----------------------------------------------------------------------------
def readBoatTable():
    bt = Boat()
    (dbStatus, boats)  = bt.readBoats(con)
    if (dbStatus == False):
        return render_template('error.html', error = bt.error)
    else:
        return(boats)
    
#----------------------------------------------------------------------------
# Procedure to read the Route table and populate the list before
# rendering in the schedule details page
#----------------------------------------------------------------------------   
def readRouteTable():
    rt = Route()
    (dbStatus, routes)  = rt.readRoutes(con)
    if (dbStatus == False):
        return render_template('error.html', error = rt.error)
    else:
        return(routes)
       


#-----------------------------------------------------------------------------
# Home page function
#-----------------------------------------------------------------------------
# For index.html default to show the cruises in the next two weeks
@app.route("/")
def index():
    global con
    
    # set debugging for this function
    db.enabled = True
    
    # set the adminstrator session varaible to False.  This gets set when
    # the user logs in as an adminstrator which means they can maintain
    # schedules
    
    session['administrator'] = False
    
    #if not session['administrator']:
    #    session['administrator'] = False
    
    # Create a schedule object.
    sched = Schedule()
    
    # Default the view of schedules to the next two weeks on the home page
    # the 'Booking' page will display everything setup for the next two years
    startDate = datetime.now().strftime("%Y-%m-%d")  
    # Add two weeks to get the future schedules
    endDate = (datetime.now() + relativedelta(weeks=2)).strftime("%Y-%m-%d")
    
    # ***** for the purposes of this project we will set the dates to where
    # ***** we know there is data in the database.
    if db.enabled == True:
        startDate = '2017-10-16'
        endDate = '2017-10-17' 
    
    # read the schedule cruises with the dates specified
    (dbStatus, rows) = sched.readSchedulebyDate(con, startDate, endDate)
    
    # If we have any error returned the throw to the generic error page
    if (dbStatus == True):
        return render_template('index.html', rows = rows)
    else:
        return render_template('error.html', error = sched.error)


# ************************************************
# Do we need the next two functions
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
 # ************************************************

#----------------------------------------------------------------
# Show the scheduled cruises in the next two years available
# for bookings
#----------------------------------------------------------------
@app.route("/bookings/")
def bookings():
    global con
    
    # set debugging
    db.enabled = True
    
    # create a schedule object
    sched = Schedule()
    
    startDate = datetime.now().strftime("%Y-%m-%d")  
    # Add two years to get the future schedules
    endDate = (datetime.now() + relativedelta(years=2)).strftime("%Y-%m-%d")

    # read the scheduled cruises between the specified dates    
    (dbStatus, rows) = sched.readSchedulebyDate(con, startDate, endDate)
    
    # Go to the generic error page if something unexpected happens, otherwise
    # show the schedules.
    if (dbStatus == True):
        return render_template("bookings.html", rows = rows)
    else:
        return render_template('error.html', error = sched.error)


#-----------------------------------------------------------------------
# Function for handling a single booking.  Get the cruiseDate and number
# and pass onto the singlebooking screen 
#-----------------------------------------------------------------------
@app.route("/singlebooking/", methods = ['POST'])
def singlebooking():
    global con
    db.enabled = True
    
    # create a schedule object
    sched = Schedule()
     
    if request.method == 'POST':
        
        # The value of the booking button contains the CruiseDate and CruiseNo seperated by
        # a '.'
        CruiseDate = request.form['booking'].split('.')[0]
        CruiseNo = int(request.form['booking'].split('.')[1])
        
        # Save the Cruisedate and CruiseNo in session variables to use later on.
        session['CruiseDate'] = CruiseDate
        session['CruiseNo'] = CruiseNo
        # do the same with adults and children
        session['adults'] = 0
        session['children'] = 0
        
        db.print('CruiseDate = ' +  session['CruiseDate'])
        db.print('CruiseNo = ' + str(session['CruiseNo']))        
 
        # Read this schedule record and pass onto the single booking page
        # The schedule object will validate that the CruiseDate and CruiseNo
        # are in the format they it needs
        (dbStatus, rows) = sched.readSched(con, CruiseDate, CruiseNo)
   
        # if there was an error returned then go to the error page and display the error. 
        if (dbStatus == True):
            return render_template("singlebooking.html", rows = rows, validationerror = '', emailaddr = '', adults = 0, children = 0)
        else:
            return render_template('error.html', error = sched.error) 

#------------------------------------------------------------------------------------------
# Function to process the data entered by the user for the single booking
# If the customer exists then we will go to the confirm booking page
# otherwise we will go to the newcustomer page where they can enter details
# before returning to complet the booking
#-------------------------------------------------------------------------------------------        
@app.route("/validatecust/", methods = ['POST'])
def validatecust():
    global con
    # set debugging
    db.enabled = True
    
    # Create an customer object, default country to NZL
    cust = Customer(con,'NZL')
    emailaddr = None
    
    if request.method == 'POST':
        
        # Get the email address entered
        emailaddr = request.form['emailAddress']
        
        # If we have returned from the customer details screen to confirm the booking then
        # just get the adults and children from the session variables.  otherwise get them
        # from the form.
        if 'bookingfromCust' in request.form:
            adults = session['adults']
            children = session['children']
        else:    
            try:
                adults = int(request.form['adults'])
            except:
                adults = 0
            try:           
                children = int(request.form['children'])
            except:
                children = 0
        
            session['adults'] = adults
            session['children'] = children
            
        # Debugging code
        db.print("--- validatecust ---")
        db.print('emailaddr = ' + emailaddr)
        db.print('CruiseDate = ' +  session['CruiseDate'])
        db.print('CruiseNo = ' + str(session['CruiseNo']))
        db.print('adults = ' + str(adults))
        db.print('children = ' + str(children))
    
        # Create a schedule object and read the schedule the are looking to book. Expect to
        # find it OK, but if something has happened then go to the error screen
        sched = Schedule()
        (dbStatus, rows) = sched.readSched(con, session['CruiseDate'], session['CruiseNo'])   
        if (dbStatus == False):
            return render_template('error.html', error = sched.error)       
        
        # let's just see if they have selected at least one adult.  create an error if they haven't and
        # re-render the same template
        if adults == 0:
            return render_template("singlebooking.html", rows = rows, validationerror = 'Need to choose at least one adult', emailaddr = emailaddr, adults = adults, children = children)
     
        # make sure there are enough seats for this booking
        if (adults + children) > sched.available:
            return render_template("singlebooking.html", rows = rows, validationerror = 'Not enough seats available', emailaddr = emailaddr, adults = adults, children = children)
            
        # If there's no email address just go to the new customer page, so they can register as a customer
        if emailaddr == None:
            countries = readCountryTable()
            return render_template("newcustomer.html", emailaddr = emailaddr, cust = custmr[0], countries = countries, action = 'ADD')
        
        # If they have entered an email address the check to see whether this customer is there 
        (dbStatus, custmr) = cust.readCustbyEmail(con, emailaddr)
        # If we got an error then check it's not that a customer couldn't be foud which is possible
        if (dbStatus == False):
            if cust.error[0:24] == 'No customer record found':
                # This could be a new customer so lets check the email address is OK
                # If it's not return an error, else go to the new customer page.
                email = Email(emailaddr)
                # Is this a Valid email address?  If not then return to our page with the error message
                # otherwise go to the new customer page setting the Action to ADD so it can be used by the newcustomer page
                if not email.validEmailAddress():
                    return render_template("singlebooking.html", rows = rows, validationerror = email.error, emailaddr = emailaddr, adults = adults, children = children)
                else:
                    countries = readCountryTable()
                    return render_template("newcustomer.html", emailaddr = emailaddr, cust = custmr[0], countries = countries, action = 'ADD')
            else:
                return render_template('error.html', error = cust.error) 
        else:
            # Only one customer will match so send the first row returned from the readbyCust routine
            # Also pass the adults and children entered.  these get passed back when they Confirm the booking
            print('Calling Customer ID: ', cust.CustID)
            return render_template("confirmbooking.html", cust = custmr[0], rows = rows, adults = adults, children = children, CustID = cust.CustID)

#------------------------------------------------------------------------------------------
# Confirm the booking with the customer and update the booking, customer and schedule
# records.
#------------------------------------------------------------------------------------------
@app.route("/confirmed/", methods = ['POST'])
def confirmed():
    global con
    
    db.enabled = True
    
    # Process data from the form     
    if request.method == 'POST':
          
        # reread the values we sent to the webpage
        adults = session['adults']
        children = session['children']
        CustID = int(request.form['CustID'])
       
        db.print("--- confirmed ---")
        db.print ("Adults = " + str(adults))
        db.print ("Children = " + str(children))
        db.print ("CustID = " + str(CustID))
        
        # Read the customer records. Create a new customer object
        cust = Customer(con,'NZL')
        (dbStatus, custmr) = cust.readCust(con,CustID)
        if (dbStatus == False):
            return render_template('error.html', error = cust.error)
       
        db.print(" * Inital read of customer * ")
        db.print("Total booking = " + str(cust.totalBookings))
        db.print("Last Booking = " + str(cust.lastBooking))
        
        # if they are updating Customer details then we will take them to the newcustomer page prefilled
        # with their exsiting details and telling the form we are Updating.
        if 'update' in request.form:
            db.print(" * Update pressed *")
            countries = readCountryTable()
            return render_template("newcustomer.html", emailaddr = cust.emailAddr, cust = custmr[0], countries = countries, CustID = CustID, action = 'UPDATE')
    
        
        # If they pressed confirm then we will confirm the booking
        if 'confirm' in request.form:
            db.print(" * Confirm pressed *")
            # create a booking object
            book = Booking()
       
            # debugging information
            db.print(" Data for booking ")
            db.print("CruiseDate = " + str(session['CruiseDate']))
            db.print("CruiseNo = " + str(session['CruiseNo']))
            db.print("Adults = " + str(session['adults']))
            db.print("Children = " + str(session['children']))
            db.print("CustID = " + str(request.form['CustID']))
    
            # Read the Schedule records
            sched = Schedule()
            (dbStatus, rows) = sched.readSched(con, session['CruiseDate'], session['CruiseNo'])
            if dbStatus == False:
                return render_template('error.html', error = sched.error)   
           
            # make sure there are enough seats for this booking, even though we checked when selecting the seats
            # it could have changed.
            if (adults + children) > sched.available:
                return render_template("confirmbooking.html", cust = custmr[0], adults = adults, children = children, custID = cust.CustID, bookingmessage = 'Not enough seats available')
                  
            # set the properties for a new booking        
            book.CruiseDate = session['CruiseDate']
            book.CruiseNo = session['CruiseNo']
            book.CustID = CustID
            book.adults = session['adults']
            book.children = session['children']
            
            # Insert the booking
            dbStatus = book.insertBooking(con)
            db.print(" * after insert booking dbStatus = " + str(dbStatus))
            if dbStatus == True:
                # all successful so set the customer and schedule records with the booking details
                cust.newBooking()
                # print debugging if turned on
                db.print(" * Inital read of customer * ")
                db.print("Total booking = " + str(cust.totalBookings))
                db.print("Last booking = " + str(cust.lastBooking))
     
                # set the schedule
                sched.newBooking(adults + children)
                db.print(" * after new booking *")
             
                # update Customer with booking details
                dbStatus = cust.updateCust(con,CustID)
                db.print(" * after cust update dbStatus = " + str(dbStatus))
                if dbStatus == False:
                    return render_template("confirmbooking.html", cust = custmr[0], rows = rows, adults = adults, children = children, custID = cust.CustID, bookingmessage = cust.error)                    
                else:
                    # update schedule with the booking details
                    dbStatus = sched.updateSchedule(con,session['CruiseDate'],session['CruiseNo'])
                    if dbStatus == False:
                        return render_template("confirmbooking.html", cust = custmr[0], rows = rows, adults = adults, children = children, custID = cust.CustID, bookingmessage = sched.error)                         
                    else:
                        # Reread the schedule record with the updated available seats
                        (dbStatus, rows) = sched.readSched(con, session['CruiseDate'], session['CruiseNo'])
                        if dbStatus == False:
                            return render_template('error.html', error = sched.error)   
                        return render_template("successbooking.html", rows = rows, adults = adults, children = children, bookingID = book.BookingID)
            else:
                 return render_template("confirmbooking.html", cust = custmr[0], adults = adults, children = children, custID = cust.CustID, bookingmessage = book.error)


#------------------------------------------------------------------------------------------
# Insert or update a customer record
#------------------------------------------------------------------------------------------
@app.route("/custdetails/", methods = ['POST'])
def custdetails():       
    global con
    
    # set debugging on or off
    db.enabled = False
    
    usercust = {}
  
    # Assign a 'usercust' dictionary which we can use to 
    # render back to the form with the values entered by the user  
    def setuserdata():
        usercust['emailaddr'] = request.form['emailaddr']
        usercust['surname'] = request.form['surname']
        usercust['firstname'] = request.form['firstname']
        usercust['DOB'] = request.form['DOB']      
        usercust['gender'] = request.form['gender']      
        usercust['phone'] = request.form['phone']
        usercust['countryCode'] = request.form['countryCode']
        
    # set the customer properties from the page. we don't need
    # to do any validation here as the customer object will do
    # all of that and return any any errors.      
    def setcustvalues():
        cust.emailAddr = usercust['emailaddr']
        cust.surname = usercust['surname'] 
        cust.firstname = usercust['firstname'] 
        cust.dob = usercust['DOB']      
        cust.gender = usercust['gender'] 
        cust.phone = usercust['phone'] 
        cust.countryCode = usercust['countryCode']         
    
    # Process input from the form  
    if request.method == 'POST':
        
        # create a new customner object
        cust = Customer(con,'NZL')
        
        # keep the data from the form
        setuserdata()
        
        # If we are updating then update the customer record
        if request.form['action'] == 'UPDATE':
            
            (dbStatus, custmr) = cust.readCustbyEmail(con, request.form['emailaddr'])
            if dbStatus == False:
                return render_template("newcustomer.html", emailaddr = cust.emailAddr, cust = usercust, countries = countries, action = 'UPDATE',returnmessage = cust.error)
   
            # set the values for the customer 
            setcustvalues()

            # reread the countries table to be able to rerender the page. if we get an error re-render teh page with any error messages
            countries = readCountryTable()
            dbStatus = cust.updateCust(con,cust.CustID)
            if dbStatus == False:
                return render_template("newcustomer.html", emailaddr = cust.emailAddr, cust = usercust, countries = countries, CustID = cust.CustID, action = 'UPDATE',returnmessage = cust.error)
            else:
                return render_template("newcustomer.html", emailaddr = cust.emailAddr, cust = usercust, countries = countries, CustID = cust.CustID, action = 'UPDATE',returnmessage = 'Customer successfully updated')
 
        if request.form['action'] == 'ADD':
            # Make sure the record isn't there.
            (dbStatus, custmr) = cust.readCustbyEmail(con, request.form['emailaddr'])
            if dbStatus == True:
                return render_template("newcustomer.html", emailaddr = cust.emailAddr, cust = usercust, countries = countries, action = 'ADD',returnmessage = 'Customer already exists')
            
            # set the customer properties from the page. 
            setcustvalues()

            # reread the countries table to be able to rerender the page 
            countries = readCountryTable()

            dbStatus = cust.insertCust(con)
            if dbStatus == False:
                return render_template("newcustomer.html", emailaddr = cust.emailAddr, cust = usercust, countries = countries, action = 'ADD',returnmessage = cust.error)
            else:
                # if the add was successful the re render the page in update mode in case they want to correct any details
                return render_template("newcustomer.html", emailaddr = cust.emailAddr, cust = usercust, countries = countries, CustID = cust.CustID, action = 'UPDATE',returnmessage = 'Customer successfully added')       


#------------------------------------------------------------------------------------------
# Insert or update a schedule record
#------------------------------------------------------------------------------------------
@app.route("/confirmschedule/", methods = ['POST'])
def confirmschedule():
    global con
    
    # set debugging level
    db.enabled = True
    db.print(" ---confirmschedule ---")
    
    # If we aren't logged in here then do not let the user get any further 
    if not session['administrator']:
        return render_template('error.html', error = "Only Administrators can access schedules")  
    
    usersched = {}
  
    # Assign a 'usersched' dictionary which we can
    # render back to the form with the values entered by the user  
    def setuserdata():
        usersched['CruiseDate'] = request.form['CruiseDate']
        usersched['CruiseNo'] = request.form['CruiseNo']
        usersched['departure'] = request.form['departure']
        usersched['BoatID'] = request.form['BoatID']      
        usersched['RouteID'] = request.form['RouteID']      
        usersched['return'] = request.form['return']
        try:
            usersched['available'] = int(request.form['available'])
        except:
           usersched['available'] = 0 
        
    # set the schedule properties from the page. we don't need
    # to do any validation here as the schedule object will do
    # all of that and return any any errors.      
    def setschedvalues():
        sched.CruiseDate = usersched['CruiseDate']
        sched.CruiseNo = usersched['CruiseNo']
        sched.departure = usersched['departure']
        sched.BoatID = usersched['BoatID']     
        sched.RouteID = usersched['RouteID'] 
        sched.returntime = usersched['return']
        sched.available = usersched['available']      
     
    # pocess the data sent from this page
    if request.method == 'POST':
                
        # create a scheule object        
        sched = Schedule()
        
        # keep the user data to diaply back if necessary
        setuserdata()
        
        # Read the boats and schedule to display in option lists      
        boats = readBoatTable()
        routes = readRouteTable()
        
        # set the scheule properties            
        setschedvalues()
                
        # If they selected the 'read' button then read this schedule record and pass back to user.
        # If not found then set the form to blank, except for the cruise date and number attempting to be found
        if 'read' in request.form:
            (dbStatus, rows) = sched.readSched(con, request.form['CruiseDate'], request.form['CruiseNo'])
            if dbStatus == False:
                rows = sched.blankScheduleRow()
            return render_template("newschedule.html",  sched = rows[0],  CruiseDate = request.form['CruiseDate'], CruiseNo = request.form['CruiseNo'], boats = boats, routes = routes,returnmessage = sched.error)        

        # If updating, call the updateSchedule method and then return any error
        if 'update' in request.form:
            db.print(" * Processing update *")
            dbStatus = sched.updateSchedule(con, request.form['CruiseDate'], request.form['CruiseNo'])
            return render_template("newschedule.html", sched = usersched, CruiseDate = request.form['CruiseDate'], CruiseNo = request.form['CruiseNo'], boats = boats, routes = routes, returnmessage = sched.error)
 
        # If deleting blank the screen if successful otherwise return the error message
        if 'delete' in request.form:
            db.print(" * Processing delete *")
            # let's check to see if there are any bookings
            book = Booking()
            (dbStatus, bookings) = book.readBookingbySched(con,request.form['CruiseDate'], request.form['CruiseNo'])
            if dbStatus == False:
                db.print("Booking error = " + book.error)
                # If there are no bookings then proceed with the delete
                if book.error[0:30] == 'No Bookings found for schedule':
                    dbStatus = sched.deleteSchedule(con, request.form['CruiseDate'], request.form['CruiseNo'])
                    if dbStatus == False:
                        return render_template("newschedule.html", sched = usersched, CruiseDate = request.form['CruiseDate'], CruiseNo = request.form['CruiseNo'], boats = boats, routes = routes, returnmessage = sched.error)
                    else:
                        rows = sched.blankScheduleRow()
                        return render_template("newschedule.html", sched = rows[0], CruiseDate = None, CruiseNo = None, boats = boats, routes = routes, returnmessage = sched.error)
                else:
                    return render_template("newschedule.html", sched = usersched, CruiseDate = request.form['CruiseDate'], CruiseNo = request.form['CruiseNo'], boats = boats, routes = routes, returnmessage = book.error)
            else:
                return render_template("newschedule.html", sched = usersched, CruiseDate = request.form['CruiseDate'], CruiseNo = request.form['CruiseNo'], boats = boats, routes = routes, action='CONFIRM', returnmessage = 'Schedule contains bookings, press confirm to delete')
    
        # If we are confirming a delete then simple delete the schedule and let the cascade rule in the database delete all the bookings.
        if 'confirmdelete' in request.form:
            db.print(" * Processing confirm delete *")
            dbStatus = sched.deleteSchedule(con, request.form['CruiseDate'], request.form['CruiseNo'])
            if dbStatus == False:
                return render_template("newschedule.html", sched = usersched, CruiseDate = request.form['CruiseDate'], CruiseNo = request.form['CruiseNo'], boats = boats, routes = routes, returnmessage = sched.error)
            else:
                rows = sched.blankScheduleRow()
                return render_template("newschedule.html", sched = rows, CruiseDate = None, CruiseNo = None, boats = boats, routes = routes, returnmessage = sched.error)
        # If they have canceled a delete, just rerender the page
        
        if 'canceldelete' in request.form:
            db.print(" * Processing cancel delete *")
            return render_template("newschedule.html", sched = usersched, CruiseDate = request.form['CruiseDate'], CruiseNo = request.form['CruiseNo'], boats = boats, routes = routes, returnmessage = sched.error)
        
        # If adding then call the insertSchedule method and let it hande any errors
        if 'add' in request.form:
            db.print(" * Processing add *")
            db.print("CruiseDate = " + request.form['CruiseDate'])
            db.print("CruiseNo = " + str(request.form['CruiseNo']))
            
            # Make sure schedule has not been added while they have been adding data to the screen.
            (dbStatus, schdle) = sched.readSched(con, request.form['CruiseDate'], request.form['CruiseNo'])
            if dbStatus == True:
                return render_template("newschedule.html",  sched = usersched,  CruiseDate = request.form['CruiseDate'], CruiseNo = request.form['CruiseNo'], boats = boats, routes = routes, returnmessage = 'Schedule already exists!')
            
            # set the schedule properties from the page.           
            setschedvalues()

            todaysDate = datetime.now().strftime("%Y-%m-%d")
            if request.form['CruiseDate'] < todaysDate:
                return render_template("newschedule.html", sched = usersched,  CruiseDate = request.form['CruiseDate'], CruiseNo = request.form['CruiseNo'], boats = boats, routes = routes,returnmessage = 'Cannot add schedule in the past')            

            # Create a boat object            
            boat = Boat()

            # and check it exists OK
            (dbStatus, thisboat) = boat.readBoatByID(con, sched.BoatID)
            if dbStatus == False:
                return render_template('error.html', error = boat.error)
            
            # Don't allow a boat to exceed capacity
            if sched.available > boat.capacity:
                return render_template("newschedule.html", sched = usersched,  CruiseDate = request.form['CruiseDate'], CruiseNo = request.form['CruiseNo'], boats = boats, routes = routes,returnmessage = 'Available seats exceeds boat capacity of ' + str(boat.capacity))   

            # insert a schedule.  any errors will just get rendered back to this page
            dbStatus = sched.insertSchedule(con)
            return render_template("newschedule.html", sched = usersched,  CruiseDate = request.form['CruiseDate'], CruiseNo = request.form['CruiseNo'], boats = boats, routes = routes,returnmessage = sched.error)
            

#------------------------------------------------------------------------------------------
# display the schedules
#------------------------------------------------------------------------------------------
@app.route("/schedules/", methods = ['GET','POST'])
def schedules():
    global con
    
    # set debugging
    db.enabled = False
    
    # check that they have logged into the system.
    if not session['administrator']:
        return render_template('error.html', error = "Only Administrators can access schedules")        
    
    schedRows = None
    Status = None
    #Create new schedule object.
    sched = Schedule()
    #Return cruise schedules between dates. Make the lower one today and
    # then put the last one two years out
    
    today = datetime.now().strftime("%Y-%m-%d")  
    # Add two years to get the future schedules
    future = (datetime.now() + relativedelta(years=2)).strftime("%Y-%m-%d")
    
    db.print(" ---schedules---")
    db.print("Today = " + today)
    db.print("Future = " + future)
    
    (Status, schedRows) = sched.readSchedulebyDate(con,today, future)
    if (Status == True):
        return render_template("schedules.html", rows = schedRows)
    else:
        return render_template('error.html', error = sched.error)

#------------------------------------------------------------------------------------------
# if the user has chosen an existing schedule then display the details for edit, otherwise
# if they have chosed to add a schedule go to the new schedule page for an insert
#------------------------------------------------------------------------------------------
@app.route("/editschedule/", methods = ['POST'])
def editschedule():
    global con
   
    # set debugging level
    db.enabled = False
    
    # Only administrators have access to this page
    if not session['administrator']:
        return render_template('error.html', error = "Only Administrators can access schedules")      
    
    # create the objects we need
    sched = Schedule()
    bt = Boat()
    rt = Route()
     
    # process the data sent back from the form 
    if request.method == 'POST':
  
        # Read the boats and schedule to display in option lists      
        boats = readBoatTable()
        routes = readRouteTable()
       
        # If they processed the edit button then read the scchedule record and pass the details
        # to the new schedule scren
        if 'Edit' in request.form:
            CruiseDate = request.form['Edit'].split('.')[0]
            CruiseNo = int(request.form['Edit'].split('.')[1])
            
            (dbStatus, rows) = sched.readSched(con, CruiseDate,CruiseNo)
            if dbStatus == False:
#                return render_template("newschedule.html",  sched = rows,  CruiseDate = CruiseDate, CruiseNo = CruiseNo, boats = boats, routes = routes, action = 'UPDATE', returnmessage = sched.error)
                return render_template("newschedule.html",  sched = rows, CruiseDate = CruiseDate, CruiseNo = CruiseNo, boats = boats, routes = routes, action = 'UPDATE', returnmessage = sched.error)
            else:
                return render_template("newschedule.html", sched = rows[0], CruiseDate = CruiseDate, CruiseNo = CruiseNo, boats = boats, routes = routes, action = 'UPDATE')
        # If they have pressed add then create a blank 'rows' record and pass to the newschedule form
        if 'Add' in request.form:
            rows = sched.blankScheduleRow()
            CruiseDate = rows[0]["CruiseDate"]
            CruiseNo = int(rows[0]["CruiseNo"])
            return render_template("newschedule.html", sched = rows, CruiseDate = CruiseDate, CruiseNo = CruiseNo, boats = boats, routes = routes, action = 'ADD')

 


# ****** any of these required *******
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
# *****************************************



@app.route("/adminlogin/")
def admin_login():
    #login template
    return render_template("adminlogin.html")

@app.route("/admin/", methods = ['POST'])
def admin():
    global con
    # create a login object
    log = Login()
    # create a schedule object
    sched = Schedule()
    schedRows = None
    Status = None
    
    # set debugging level
    db.enabled = False    
    
    #variables pulled from the html form to pass to the login object
    UserCode = request.form['Usercode']
    password = request.form['Password']
    
    #pass variables to login object allowing password to be authenticated
    (db.status) = log.AuthLoginByUserCode(con, UserCode, password)
    
    #Return cruise schedules between dates. Make the lower one today and
    # then put the last one two years out
    today = datetime.now().strftime("%Y-%m-%d")  
    # Add two years to get the future schedules
    future = (datetime.now() + relativedelta(years=2)).strftime("%Y-%m-%d")
    
    db.print(" ---schedules---")
    db.print("Today = " + today)
    db.print("Future = " + future)
    
    (Status, schedRows) = sched.readSchedulebyDate(con,today, future)
    
    #if password and schedule is valid render the schedules template
    if db.status == True and Status == True:
        session['administrator'] = True
        return render_template("schedules.html", rows = schedRows, validationerror = '')
    else:
        #else rerender the login template and display the appropriate error
        return render_template("adminlogin.html", rows = rows, validationerror = log.error)

@app.route("/not_available")
def na():
    #placeholder while pages are developed
    return render_template("not_available.html")

if __name__ == "__main__":
    app.run()
#cd 2017\DTP\Fox_II_Website
#c:\Python34\python.exe app2.py

# Import standard Python modules
import sqlite3
from flask import Flask, render_template, request, session
app = Flask(__name__, template_folder="templates")

# Import custom modules here.
from customer import Customer
from schedule import Schedule
from booking import Booking
from emailAddress import Email

# require a secret key for session data to work OK.  Just needs
# to be a random 20 characters
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

# set a global varibale to allow database connection to be used
# throughout the program
global con


# Make a connection to the database
con = sqlite3.connect('database/Fox_II.db')
#Makes sure foreign keys are enforce for database integrity
con.execute('pragma foreign_keys=ON')

print ("Opened database successfully") #Confirm database connection.
#con.close()

# For index.html default to show the cruises in the next two weeks
@app.route("/")
def index():
    global con
    # Create a schedule object.
    sched = Schedule()
    
    startDate = '2017-10-16'
    endDate = '2017-10-17'
    
    (dbStatus, rows) = sched.readSchedulebyDate(con, startDate, endDate)
    
    # If we have any error returned the throw to error page
    if (dbStatus == True):
        return render_template('index.html', rows = rows)
    else:
        return render_template('erorr.html', error = sched.error)


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

### Do we use this???
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
        return render_template('error.html', error = sched.error)

# User has chose a booking so get the cruise details and display the cruise
@app.route("/singlebooking/", methods = ['POST'])
def singlebooking():
    global con
    sched = Schedule()
     
    if request.method == 'POST':
        CruiseDate = request.form['label'].split('.')[0]
        CruiseNo = int(request.form['label'].split('.')[1])
        # Save the Cruisedate and CruiseNo in session variables to use later on.
        session['CruiseDate'] = CruiseDate
        session['CruiseNo'] = CruiseNo
 
        # Read this schedule record and pass onto the single booking page  
        (dbStatus, rows) = sched.readSched(con, CruiseDate, CruiseNo)
   
        # if there was an error returned then go to the error page and display the error. 
        if (dbStatus == True):
            return render_template("singlebooking.html", rows = rows, validationerror = '', emailaddr = '')
        else:
            return render_template('error.html', error = sched.error) 
        
# Validate the email address entered for a booking and check to see whether its and
# existing cstomer or not.  If it's an exisitng customer then we will simply go to
# confirm the booking, otherwise take them to a new customer page where they can add
# their details before going to confirm the booking.
# Also do some basic validation checks to make sure that their are enough seats and
# there is at least one adult.  If these checks fail we just render the same page with an
# error message.
@app.route("/validatecust/", methods = ['POST'])
def validatecust():
    global con
    # Create an customer object
    cust = Customer()
    emailaddr = None
    
    if request.method == 'POST':
        emailaddr = request.form['emailAddress']
        adults = int(request.form['adults'])
        children = int(request.form['children'])
        
        print('email: ',emailaddr)
        print('CruiseDate: ', session['CruiseDate'])
        print('CruiseNo: ',session['CruiseNo'])
    
        # Create a schedule object and read the schedule the are looking to book
        sched = Schedule()
        (dbStatus, rows) = sched.readSched(con, session['CruiseDate'], session['CruiseNo'])   
        if (dbStatus == False):
            return render_template('error.html', error = sched.error)       
        
        # let's just see if they have selected at least one adult.  create an error if they haven't.
        if adults == 0:
            return render_template("singlebooking.html", rows = rows, validationerror = 'Need to choose at least one adult', emailaddr = emailaddr)
     
        # make sure there are enough seats for this booking
        if (adults + children) > sched.available:
            return render_template("singlebooking.html", rows = rows, validationerror = 'Not enough seats available', emailaddr = emailaddr)
            
        # If there's no email address just go to the new customer page
        if emailaddr == None:
            return render_template("newcustomer.html", emailaddr = emailaddr)
        
        # Check to see whether this customer is there using the email address.
        (dbStatus, custmr) = cust.readCustbyEmail(con, emailaddr)
        # If we got an error then check it's not that a customer couldn't
        # be found which is possible.
        if (dbStatus == False):
            if cust.error[0:24] == 'No customer record found':
                # This could be a new customer so lets check the email address is OK
                # If it's not return an error, else go to the new customer page.
                email = Email(emailaddr)
                # Is this a Valid email address?  If not then return to our page with the error message
                # otherwise go to the new customer page.
                if not email.validEmailAddress():
                    return render_template("singlebooking.html", rows = rows, validationerror = email.error, emailaddr = emailaddr)
                else:
                    return render_template("newcustomer.html", emailaddr = emailaddr, action = 'ADD')
            else:
                return render_template('error.html', error = cust.error) 
        else:
            # Only one customer will match so send the first row
            return render_template("confirmbooking.html", cust = custmr[0], rows = rows, adults = adults, children = children, custID = cust.CustID)


# Validate the email address entered for a book and check to see whether its and
# existing cstomer or not
@app.route("/confirmed/", methods = ['POST'])
def confirmed():
    global con
    # Create an customer object
    cust = Customer()

    if 'update' in request.form:
        return render_template("newcustomer.html", emailaddr = emailaddr, cust = custmr[0], action = 'UPDATE')
        print("Update Pressed")
    
    if 'confirm' in request.form:
        print("Confirm pressed")
        
    if 'adults' in request.form:
        print('Adults present:', request.form['adults'])


# Not sure need this??
@app.route("/custdetails/", methods = ['POST'])
def custdetails():
        
    return render_template("custdetails.html", custname = custname)





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
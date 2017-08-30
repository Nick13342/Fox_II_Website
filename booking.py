import sqlite3
from datetime import datetime

#------------------------------------------------------------------------------------
# Class Name: Booking
# Written By: Nick Glanville
# Date:       26-07-2017
#
# Class to create allow an instance of an Booking object.  This class is designed to
# perform all of the basic database functions on the bookings table. 
#------------------------------------------------------------------------------------

class Booking:
    
   
    #---------------------------------------------------------------------------------
    # Initialise instance of booking
    #---------------------------------------------------------------------------------
    def __init__(self):      
        self.__nullBooking()
        
  
    #---------------------------------------------------------------------------------
    # Initialse a blank Schedule structure
    #---------------------------------------------------------------------------------
    def __nullBooking(self):
        # Create blank instance variables for the new created object here.  We will
        # prefix these with a single '_' to make clear that they are internal to this class.
        self._BookingID = 0
        self._CruiseDate = None
        self._CruiseNo = 0
        self._CustID = 0
        self._BookingDate = None
        self._adults = 0
        self._children = 0
    
    #---------------------------------------------------------------------------------
    #  Internal function to set the property values to the current row.  The __ at the
    #  start of the dunction indicate that it cannot be access for any calling programs
    #---------------------------------------------------------------------------------     
    def __setBooking(self,row):
        # Allocate the retrieved columns into the object variables.
        self._BookingID = row['BookingID']
        self._CruiseDate = row['CruiseDate']
        self._CruiseNo = row['CruiseNo']
        self._CustID = row['CustID']
        self._BookingDate = row['BookingDate']
        self._available = row['adults']
        self._status = row['children']
    
    #---------------------------------------------------------------------------------
    #  Internal function to check the date or time format.  Usually we expect that the 
    #  incoming value has been successfully validated, but this final check will ensure 
    #  database integrity in the event that it hasn't been validated correctly
    #---------------------------------------------------------------------------------       
    def __validateDT(self,date_text, format):
        try:
            # Take the date_text and return a datetime value formatted as supplied to the function.
            # Reformatting the string back ensure we have the format we require, including leading
            # 0's. eg 09:04, 2017-03-02
            # If there is anerror converting the date with strptime, then a Value error execption
            # is raised.  If the dates don't match we raise the ValueError eception as well so
            # it can be handled in the same way
            if date_text != datetime.strptime(date_text, format).strftime(format):
                raise ValueError
            return True
        except ValueError:
            return False   
           
    #-----------------------------------------------------------------------------------------------
    # Read a customer record from the database.  Required is the database handle and the Customer ID
    #-----------------------------------------------------------------------------------------------
    def readBookingbyCustomer(self, con, CustID):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        rows = []
        # Make sure we nulled all of the entries for the booking before the read.
        self.__nullBooking()       
        
        # define SQL query
        read_query = "SELECT b.BookingID, b.CruiseDate, b.CruiseNo, b.BookingDate, b.CustID, b.adults, b.children \
                     FROM bookings b \
                     WHERE b.CustID = ?"
       
        try:
            # define cursone and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query, (CustID,))
        
            rows = cur.fetchall();
            
            if not rows:
                self._error = "No Bookings record found for customer: " + str(CustID)
                self._retvalue = False
       
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
            
        return (self._retvalue, rows)
    
    
    #-------------------------------------------------------------------------------------------------
    # Insert a new booking using the property values for the booking which need to have been
    # set by the calling program.
    #-------------------------------------------------------------------------------------------------
    def insertBooking(self, con):
        # retValue contains the success or failure of the update operation. Default to success
        self._retvalue = True
        self._error = None
        
        # Do any data validation checks here to ensure database integrity.  Some fields will be handled by
        # constraints within the database itself.
        if self._CruiseDate:
            if not self.__validateDT(self._CruiseDate, "%Y-%m-%d"):
                self._error = "Invalid date format"
                self._retvalue = False
                return self._retvalue

        # Even though the database fields are defined as Integers, SQLite will allow string values
        # to be inserted!  
        if not isinstance(self._CruiseNo,int):
            self._error = "CruiseNo is not numeric"
            self._retvalue = False
            return self._retvalue
       
             
        if not isinstance(self._CustID, int):
            self._error = "Customer ID is not numeric"
            self._retvalue = False
            return self._retvalue
        
        if not isinstance(self._adults, int):
            self._error = "Adults value is not numeric"
            self._retvalue = False
            return self._retvalue
        
        if not isinstance(self._children, int):
            self._error = "Children value is not numeric"
            self._retvalue = False
            return self._retvalue   
        
        # set booking date to today.
        self._BookingDate = datetime.now().strftime("%Y-%m-%d")             
        
        # define SQL query
        insert_query = "insert into bookings (CruiseDate, CruiseNo, CustID, BookingDate, \
        adults, children) VALUES (?, ?, ?, ?, ?, ?)" 
    
        # attempt to execute the query        
        try:
            cur = con.cursor()
        
            cur.execute(insert_query, (self._CruiseDate, self._CruiseNo, self._CustID, \
                                self._BookingDate, self._adults, self._children))
        
            # Commit the trasaction if successful.
            con.commit()
            
            # Set the Booking ID to the lastrowid as it's an auto increment field in the database.
            self._BookingID = cur.lastrowid
            
        # Exception processing logic here.    
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            # Rollback transaction if failed.
            con.rollback()
            self._retvalue = False
                    
        return self._retvalue
    
     
    #-------------------------------------------------------------------------------------------------
    # Expose the object variables to calling programs using 'setter' and 'getter' routines instead
    # of using individual methods.  This allows us to control how the properties are set and returned
    # to the calling program.
    #------------------------------------------------------------------------------------------------- 
    
    # ------Booking ID ------
    @property
    def BookingID(self):
        return self._BookingID
    
    # ----- Cruise Date ------
    @property
    def CruiseDate(self):
        return self._CruiseDate
    
    @CruiseDate.setter
    def CruiseDate(self, CruiseDate):
        self._CruiseDate = CruiseDate 
   
    # ----- Cruise Number ------
    @property
    def CruiseNo(self):
        return self._CruiseNo
    
    @CruiseNo.setter
    def CruiseNo(self, CruiseNo):
        self._CruiseNo = CruiseNo 
    
    # ------ Customer ID ------
    @property
    def CustID(self):
        return self._CustID
 
    @CustID.setter
    def CustID(self, CustID):
        self._CustID = CustID   
    
    # ------ adults ------   
    @property
    def adults(self):
        return self._adults
   
    @adults.setter
    def adults(self, adults):
        self._adults = adults   
   
     # ------ children ------   
    @property
    def children(self):
        return self._children
   
    @children.setter
    def children(self, children):
        self._children = children   
     
   
    
    # ----- any error codes -----  
    @property
    def error(self):
        return self._error 
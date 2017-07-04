import sqlite3
import datetime

#------------------------------------------------------------------------------------
# Class Name: Customer
# Written By: Nick Glanville
# Date:       02-07-2017
#
# Class to create allow an instance of an Customer object.  This class is designed to
# perform all of the basic database functions on the Customer table.  It allows the
# calling program to call simple methods when maintaining customers.  
#------------------------------------------------------------------------------------

class Customer:
    
    #---------------------------------------------------------------------------------
    # Initialse a blank customer structure
    #---------------------------------------------------------------------------------
    def __init__(self):
        
        # Create blank instance vriables for the new created object here.  We will
        # prefix these with a single '_' to make clear that they are internal to this class.
        self._CustID = 0
        self._surname = ""
        self._firstname = ""
        self._email = ""
        self._dob = None
        self._gender = ""
        self._phone = ""
        self._countryCode = ""
        self._lastBooking = None
        self._totalBookings = 0
 
    #---------------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------------     
    def __setCustomer(self,row):
        # Allocate the retrieved columns into the object variables.
        self._email = row['Email']
        self._surname = row['surname']
        self._firstname = row['firstname']
        self._dob = row['DOB']
        self._gender = row['gender']
        self._phone = row['phone']
        self._countryCode = row['CountryCode']
        self._lastBooking = row['lastBooking']
        self._totalBookings = row['totalBookings']
    
    
    
    #-----------------------------------------------------------------------------------------------
    # Read a customer record from the database.  Required is the database handle and the Customer ID
    #-----------------------------------------------------------------------------------------------
    def readCust(self, con, CustID):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        # define SQL query
        read_query = "select * from customer where CustID = ?"
       
        try:
            # define cursone and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query, (CustID,))
        
            row = cur.fetchone();
            
            if row == None:
                self._error = "No customer record found with CustID of: " + str(CustID)
                self._retvalue = False
            else:
                self.__setCustomer(row)

            
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
            
        return self._retvalue
  
    #-----------------------------------------------------------------------------------------------
    # Read a customer record from the database by email address.  Required is the database handle
    # and email
    #-----------------------------------------------------------------------------------------------
    def readCustbyEmail(self, con, Email):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        # define SQL query
        read_query = "select * from customer where CustID = ?"
       
        try:
            # define cursone and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query, (CustID,))
        
            row = cur.fetchone();
            
            if row == None:
                self._error = "No customer record found with CustID of: " + str(CustID)
                self._retvalue = False
            else:
                self.__setCustomer(row)
            
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
            
        return self._retvalue
    
    #-------------------------------------------------------------------------------------------------
    # 
    # 
    #-------------------------------------------------------------------------------------------------
    def insertCust(self, con):
        # retValue contains the success or failure of the update operation. Default to success
        self._retvalue = True
        self._error = None
        
        # define SQL query
        update_query = "update customer set Email = ?, surname = ?," \
        "firstname = ?, DOB = ?, gender = ?, phone = ?, CountryCode = ?," \
        "lastBooking = ?, totalBookings = ? where CustID = ?"

        # attempt to execute the query        
        try:
            cur = con.cursor()
        
            cur.execute(update_query, (self._email, self._surname, self._firstname, \
                                self._dob, self._gender, self._phone, self._countryCode, \
                                self._lastBooking, self._totalBookings, CustID))        
        
            # Commit the trasaction if successful.
            con.commit()
            
        # Exception processing logic here.    
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            # Rollback transaction if failed.
            con.rollback()
            self._retvalue = False
                    
        return self._retvalue
  
  
    
    #-------------------------------------------------------------------------------------------------
    # Update a customer record from the database.  Required is the database handle and the Customer ID
    # All fields will be updated with the object variables.
    #-------------------------------------------------------------------------------------------------
    def updateCust(self, con, CustID):
        # retValue contains the success or failure of the update operation. Default to success
        self._retvalue = True
        self._error = None
        
        # define SQL query
        update_query = "update customer set Email = ?, surname = ?," \
        "firstname = ?, DOB = ?, gender = ?, phone = ?, CountryCode = ?," \
        "lastBooking = ?, totalBookings = ? where CustID = ?"

        # attempt to execute the query        
        try:
            cur = con.cursor()
        
            cur.execute(update_query, (self._email, self._surname, self._firstname, \
                                self._dob, self._gender, self._phone, self._countryCode, \
                                self._lastBooking, self._totalBookings, CustID))        
        
            # Commit the trasaction if successful.
            con.commit()
            
        # Exception processing logic here.    
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            # Rollback transaction if failed.
            con.rollback()
            self._retvalue = False
                    
        return self._retvalue
   
    #------------------------------------------------------------------------------------------------
    # If a new booking is made then we increment the total bookings and set the last booking
    # date to be today
    #------------------------------------------------------------------------------------------------
    def newBooking(self):
        self._totalBookings += 1
        self._lastBooking = datetime.date.now().strftime ("%Y-%m-%d")
   
   
    #-------------------------------------------------------------------------------------------------
    # Expose the instance variables to calling programs using 'setter' and 'getter' routines instead
    # of using individual methods.  This allows us to control how the properties are set and returned
    # to the calling program.
    # Do not create setter methods for totalBookings and lastBooking as they are controlled by the
    # newBooking method
    #------------------------------------------------------------------------------------------------- 
    
    # ----- Customer ID ------
    # Only allow a customer ID to be returned, do not allow setting as it's a system assigned field.
    @property
    def CustID(self):
        return self._CustID
    
    # ----- Email addreess ----
    @property
    def emailAddr(self):
        return self._email    
        
    @emailAddr.setter
    def emailAddr(self, emailAddr):
        self._email = emailAddr
    
    # ----- Surname -----
    @property
    def surname(self):
        return self._surname  
    
    @surname.setter
    def surname(self, surname):
        self._email = surname
    
    # ----- Firstname -----  
    @property
    def firstname(self):
        return self._firstname
    
    @firstname.setter
    def firstname(self, firstname):
        self._email = firstname
    
     # ----- Date of birth -----        
    @property
    def dob(self):
        return self._dob
    
    @dob.setter    
    def dob(self, dob):
        self._email = dob
    
    # ----- Gender -----    
    @property
    def gender(self):
        return self._gender
    
    @gender.setter    
    def gender(self, gender):
        self._email = gender
        
    # ----- Phone number ------        
    @property
    def phone(self):
        return self._phone
    
    @phone.setter    
    def phone(self, phone):
        self._phone = phone
    
    # ----- Country Code -----    
    @property
    def countryCode(self):
        return self._countryCode
    
    @countryCode.setter    
    def countryCode(self, countryCode):
        self._countryCode = countryCode
    
    # ----- lastBooking -----        
    @property
    def lastBooking(self):
        return self._lastBooking
    
    # ----- total Bookings -----        
    @property
    def totalBookings(self):
        return self._totalBookings
  
    # ----- any error codes -----  
    @property
    def error(self):
        return self._error 
  
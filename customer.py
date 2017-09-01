import sqlite3
from datetime import datetime
from emailAddress import Email
import re

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
    # Initialse a customer instance
    #---------------------------------------------------------------------------------
    def __init__(self):     
        self.__nullCustomer()
 
    #---------------------------------------------------------------------------------
    # Initialse a blank customer structure
    #---------------------------------------------------------------------------------
    def __nullCustomer(self):
        # Create blank instance vriables for the new created object here.  We will
        # prefix these with a single '_' to make clear that they are internal to this class.
        self._CustID = 0
        self._surname = ""
        self._firstname = ""
        self._email = None
        self._dob = None
        self._gender = ""
        self._phone = ""
        self._countryCode = ""
        self._lastBooking = None
        self._totalBookings = 0     
 
    #---------------------------------------------------------------------------------
    #  Internal function to set the property values to the current row.  The __ at the
    #  start of the dunction indicate that it cannot be access for any calling programs
    #---------------------------------------------------------------------------------     
    def __setCustomer(self,row):
        # Allocate the retrieved columns into the object variables.
        self._CustID = row['CustID']
        self._email = row['Email']
        self._surname = row['surname']
        self._firstname = row['firstname']
        self._dob = row['DOB']
        self._gender = row['gender']
        self._phone = row['phone']
        self._countryCode = row['CountryCode']
        self._lastBooking = row['lastBooking']
        self._totalBookings = row['totalBookings']
 
 
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
 
  
    #---------------------------------------------------------------------------------
    # Internal function to check the phone format. Just check that the phone number
    # contains recognised numbers. Use the following regulare expression
    # ^[+]?[\(\)0-9]+)+$
    # where:
    # ^ - indicates the beginning of the string
    # [+]? - allows an optional + character at the beginning of the string
    # [\(\)0-9]+ - allows any digits and parenthesis in the rest of the string
    # $ - indicates the end of the string.
    #
    # So examples of valid numbers: +123456534, +(064)26528907, 033662987
    # Examples of invalid numbers:  027-43543098 0800-TOPDOG
    #---------------------------------------------------------------------------------         
    def __validatePhoneNumber(self, phone_number):
        # Use Pythons built in Regular Epression object to compare the phone number
        pattern = re.compile("^[+]?[\(\)0-9]+$")
        if pattern.match(phone_number):
            return True
        else:
            return False
           
        
    #-----------------------------------------------------------------------------------------------
    # Read a customer record from the database.  Required is the database handle and the Customer ID
    # Retrieve the country name from the country table as linked by the countrycode.
    #-----------------------------------------------------------------------------------------------
    def readCust(self, con, CustID):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        row = []
        # Initialise the custome if this fails
        self.__nullCustomer
        
        # define SQL query. Use a UNION statement on the country table to return the name of
        # the country as well as the codes.  Instead of typing in the full name of the tables
        # an alias has been used.   

        read_query = "SELECT c.CustId, c.Email, c.DOB, c.gender, c.phone, c.surname, c.firstname, \
                    c.CountryCode, cc.country, c.lastBooking, c.totalBookings FROM customer c \
                    INNER JOIN country cc \
                    ON c.CountryCode = cc.CountryCode \
                    WHERE c.CustID = ?"
        try:
            # define cursone and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query, (CustID,))
        
            row = cur.fetchall();
            
            if row == None:
                self._error = "No customer record found with CustID of: " + str(CustID)
                self._retvalue = False
            else:
                # Only excpect one customer to be returned
                self.__setCustomer(row[0])

            
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
            
        return (self._retvalue, row)
  
    #-----------------------------------------------------------------------------------------------
    # Read a customer record from the database by email address.  Required is the database handle
    # and email
    #-----------------------------------------------------------------------------------------------
    def readCustbyEmail(self, con, Email):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        row = []
        # Initialise the custome if this fails
        self.__nullCustomer
        
        # define SQL query. Use a UNION statement on the country table to return the name of
        # the country as well as the codes.  Instead of typing in the full name of the tables
        # an alias has been used.       
        read_query = "SELECT c.CustId, c.Email, c.DOB, c.gender, c.phone, c.surname, c.firstname, \
                     c.CountryCode, cc.country, c.lastBooking, c.totalBookings FROM customer c \
                    INNER JOIN country cc \
                    ON c.CountryCode = cc.CountryCode \
                    WHERE c.Email = ?"

        try:
            # define cursone and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query, (Email,))
        
            row = cur.fetchall();
            
            if not row:
                self._error = "No customer record found with Email of: " + str(Email)
                row[0]['CustId'] = 0
                row[0]['surname'] = ""
                row[0]['firstname'] = ""
                row[0]['email'] = None
                row[0]['dob'] = None
                row[0]['gender'] = ""
                row[0]['phone'] = ""
                row[0]['countryCode'] = ""
                self._retvalue = False
            else:
                self.__setCustomer(row[0])
            
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
            
        return (self._retvalue, row)
    
    #-------------------------------------------------------------------------------------------------
    # Insert a new customer record using the property values for customer which need to have been
    # set by the calling program.
    #-------------------------------------------------------------------------------------------------
    def insertCust(self, con):
        # retValue contains the success or failure of the update operation. Default to success
        self._retvalue = True
        self._error = None

        
        # Do any data validation checks here to ensure database integrity.  Some fields will be handled by
        # constraints within the database itself.
        if self._dob:
            if not self.__validateDT(self._dob,"%Y-%m-%d"):
                self._error = "Invalid date format"
                self._retvalue = False
                return self._retvalue
 
        # Do any data validation checks here to ensure database integrity.  Some fields will be handled by
        # constraints within the database itself.
        if self._phone:
            if not self.__validatePhoneNumber(self._phone):
                self._error = "Invalid phone number format. Must only contain +, (,) and digits"
                self._retvalue = False
                return self._retvalue
           
        # Now check the new email address. First initalise a new email object with the customers email address. 
        # It's preferable if the calling program does this check, but we will also capture any errors
        # here.
        if self._email:
            thisEmail = email(self._email)
            # Use the method validEmailAddress to check the email and return any errors if found.
            if not thisEmail.validEmailAddress():
                self._error = thisEmail.error
                self._retvalue = False
                return self._retvalue
        
        # define SQL query
        insert_query = "insert into customer (Email, surname, firstname, DOB, gender, \
        phone, CountryCode, lastBooking, totalBookings) VALUES (?, ?, ?, \
                                ?, ?, ?, ?, ?, ?)" 
    
        # attempt to execute the query        
        try:
            cur = con.cursor()
        
            cur.execute(insert_query, (self._email, self._surname, self._firstname, \
                                self._dob, self._gender, self._phone, self._countryCode, \
                                self._lastBooking, self._totalBookings))        
        
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
        
        # Do any data validation checks here to ensure database integrity.  Some fields will be handled by
        # constraints within the database itself.
        if self._dob:
            if not self.__validateDT(self._dob,"%Y-%m-%d"):
                self._error = "Invalid date format"
                self._retvalue = False
                return self._retvalue
        
        # Do any data validation checks here to ensure database integrity.  Some fields will be handled by
        # constraints within the database itself.
        if self._phone:
            if not self.__validatePhoneNumber(self._phone):
                self._error = "Invalid phone number format. Must only contain +, (,) and digits"
                self._retvalue = False
                return self._retvalue
        
        # Now check the new email address. First initalise a new email object with the customers email address. 
        # It's preferable if the calling program does this check, but we will also capture any errors
        # here.
        if self._email:
            thisEmail = Email(self._email)
            # Use the method validEmailAddress to check the email and return any errors if found.
            if not thisEmail.validEmailAddress():
                self._error = thisEmail.error
                self._retvalue = False
                return self._retvalue     
        
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
        self._lastBooking = datetime.now().strftime ("%Y-%m-%d")
   
   
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
        self._surname = surname
    
    # ----- Firstname -----  
    @property
    def firstname(self):
        return self._firstname
    
    @firstname.setter
    def firstname(self, firstname):
        self._firstname = firstname
    
     # ----- Date of birth -----        
    @property
    def dob(self):
        return self._dob
    
    @dob.setter    
    def dob(self, dob):
        self._dob = dob
    
    # ----- Gender -----    
    @property
    def gender(self):
        return self._gender
    
    @gender.setter    
    def gender(self, gender):
        self._gender = gender
        
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
  
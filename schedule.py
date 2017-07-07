import sqlite3
from datetime import datetime

#------------------------------------------------------------------------------------
# Class Name: Schedule
# Written By: Nick Glanville
# Date:       07-07-2017
#
# Class to create allow an instance of an Schedule object.  This class is designed to
# perform all of the basic database functions on the Schedule table.  It allows the
# calling program to call simple methods when maintaining schedules.  
#------------------------------------------------------------------------------------

class Schedule:
    
    #---------------------------------------------------------------------------------
    # Initialse a blank Schedule structure
    #---------------------------------------------------------------------------------
    def __init__(self):
        
        # Create blank instance vriables for the new created object here.  We will
        # prefix these with a single '_' to make clear that they are internal to this class.
        self._CruiseDate = None
        self._CruiseNo = 1
        self._departure = ""
        self._BoatID = ""
        self._RouteID = ""
        self._return = ""
        self._available = 0
        self._status = ""
    
    #---------------------------------------------------------------------------------
    #  Internal function to set the property values to the current row.  The __ at the
    #  start of the dunction indicate that it cannot be access for any calling programs
    #---------------------------------------------------------------------------------     
    # def __setCustomer(self,row):
    #     # Allocate the retrieved columns into the object variables.
    #     self._email = row['Email']
    #     self._surname = row['surname']
    #     self._firstname = row['firstname']
    #     self._dob = row['DOB']
    #     self._gender = row['gender']
    #     self._phone = row['phone']
    #     self._countryCode = row['CountryCode']
    #     self._lastBooking = row['lastBooking']
    #     self._totalBookings = row['totalBookings']
    
    #---------------------------------------------------------------------------------
    #  Internal function to check the date format.  Usually we expect that the incoming
    #  date has been successfully validated, but this final check will ensure database
    #  integrity in the event that it hasn't been validated correctly
    #---------------------------------------------------------------------------------       
    def __validateDate(self,date_text):
        try:
            # take the date_text and ruturn a date time value formatted as YYYY-MM_DD. Reformatting the
            # date back with strftime ensures we have zero padded Month and Day values. If there is an
            # error convertin the date with strptime, then a Value error exection is raised.  We do the
            # same manually if the final dates don't match
            if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            return True
        except ValueError:
            return False
        
        
    #-----------------------------------------------------------------------------------------------
    # Read a customer record from the database.  Required is the database handle and the Customer ID
    #-----------------------------------------------------------------------------------------------
    # def readCust(self, con, CustID):
    #     # retValue contains the success or failure of the read operation. Default to success
    #     self._retvalue = True
    #     self._error = None
    #     # define SQL query
    #     read_query = "select * from customer where CustID = ?"
    #    
    #     try:
    #         # define cursone and execute the query, CustID is the primary key so we will only expect
    #         # one record to be returned.
    #         con.row_factory = sqlite3.Row
    #         cur = con.cursor()
    #         cur.execute(read_query, (CustID,))
    #     
    #         row = cur.fetchone();
    #         
    #         if row == None:
    #             self._error = "No customer record found with CustID of: " + str(CustID)
    #             self._retvalue = False
    #         else:
    #             self.__setCustomer(row)
    # 
    #         
    #     # Exception processing logic here.            
    #     except Exception as err:
    #         self._error = "Query Failed: " + str(err)
    #         self._retvalue = False
    #         
    #     return (self._retvalue, row)
    # 
    #-----------------------------------------------------------------------------------------------
    # Read the schedule record and return those matching the starting and ending dates as passed
    # from the calling program.
    #-----------------------------------------------------------------------------------------------
    def readSchedulebyDate(self, con, startDate, endDate):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        rows = None
        
        # Check that the dates are in a valid format and consistant with those that will be stored
        # within the Schedule table
        if not self.__validateDate(startDate) or not self.__validateDate(endDate) :
            self._error = "Invalid date format"
            self._retvalue = False
            return (self._retvalue, rows)
        
        #Check start date is less than or equal to end date.
        if startDate > endDate:
            self._error = "Start date is after end date."
            self._retvalue = False
            return (self._retvalue, rows)
        # define SQL query       
        read_query = "SELECT s.CruiseDate, s.CruiseNo, s.departure, s.BoatID, b.name, s.RouteID, \
                     r.description, s.return, s.available, s.status \
                    FROM schedule s \
                    INNER JOIN boat b \
                    ON b.BoatID = s.BoatID \
                    INNER JOIN route r \
                    ON s.RouteID = r.RouteID \
                    WHERE s.CruiseDate between ? and ? \
                    ORDER BY s.CruiseDate ASC" 
        try:
            # define cursone and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query, (startDate,endDate))
        
            rows = cur.fetchall();
            
            if rows == None:
                self._error = "No schedule records found between: " + str(startDate) + " " + str(endDate)
                self._retvalue = False
            
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
            
        return (self._retvalue, rows)
    
    #-------------------------------------------------------------------------------------------------
    # Insert a new customer record using the property values for customer which need to have been
    # set by the calling program.
    #-------------------------------------------------------------------------------------------------
    # def insertCust(self, con):
    #     # retValue contains the success or failure of the update operation. Default to success
    #     self._retvalue = True
    #     self._error = None
    #     
    #     # Do any data validation checks here to ensure database integrity.  Some fields will be handled by
    #     # constraints within the database itself.  
    #     if not self.__validateDate(self._dob):
    #         self._error = "Invalid date format"
    #         self._retvalue = False
    #         return self._retvalue
    #         
    #     
    #     # define SQL query
    #     insert_query = "insert into customer (Email, surname, firstname, DOB, gender, \
    #     phone, CountryCode, lastBooking, totalBookings) VALUES (?, ?, ?, \
    #                             ?, ?, ?, ?, ?, ?)" 
    # 
    #     # attempt to execute the query        
    #     try:
    #         cur = con.cursor()
    #     
    #         cur.execute(insert_query, (self._email, self._surname, self._firstname, \
    #                             self._dob, self._gender, self._phone, self._countryCode, \
    #                             self._lastBooking, self._totalBookings))        
    #     
    #         # Commit the trasaction if successful.
    #         con.commit()
    #         
    #     # Exception processing logic here.    
    #     except Exception as err:
    #         self._error = "Query Failed: " + str(err)
    #         # Rollback transaction if failed.
    #         con.rollback()
    #         self._retvalue = False
    #                 
    #     return self._retvalue
    # 
  
    
    #-------------------------------------------------------------------------------------------------
    # Update a customer record from the database.  Required is the database handle and the Customer ID
    # All fields will be updated with the object variables.
    #-------------------------------------------------------------------------------------------------
    # def updateCust(self, con, CustID):
    #     # retValue contains the success or failure of the update operation. Default to success
    #     self._retvalue = True
    #     self._error = None
    #     
    #     # Do any data validation checks here to ensure database integrity.  Some fields will be handled by
    #     # constraints within the database itself.  
    #     if not self.__validateDate(self._dob):
    #         self._error = "Invalid date format"
    #         self._retvalue = False
    #         return self._retvalue
    #         
    #     
    #     
    #     # define SQL query
    #     update_query = "update customer set Email = ?, surname = ?," \
    #     "firstname = ?, DOB = ?, gender = ?, phone = ?, CountryCode = ?," \
    #     "lastBooking = ?, totalBookings = ? where CustID = ?"
    # 
    #     # attempt to execute the query        
    #     try:
    #         cur = con.cursor()
    #     
    #         cur.execute(update_query, (self._email, self._surname, self._firstname, \
    #                             self._dob, self._gender, self._phone, self._countryCode, \
    #                             self._lastBooking, self._totalBookings, CustID))        
    #     
    #         # Commit the trasaction if successful.
    #         con.commit()
    #         
    #     # Exception processing logic here.    
    #     except Exception as err:
    #         self._error = "Query Failed: " + str(err)
    #         # Rollback transaction if failed.
    #         con.rollback()
    #         self._retvalue = False
    #                 
    #     return self._retvalue
   
     
    #-------------------------------------------------------------------------------------------------
    # Expose the instance variables to calling programs using 'setter' and 'getter' routines instead
    # of using individual methods.  This allows us to control how the properties are set and returned
    # to the calling program.
    # Do not create setter methods for totalBookings and lastBooking as they are controlled by the
    # newBooking method
    #------------------------------------------------------------------------------------------------- 
    
    # ----- Customer ID ------
    # Only allow a customer ID to be returned, do not allow setting as it's a system assigned field.
    # @property
    # def CustID(self):
    #     return self._CustID
    # 
    # # ----- Email addreess ----
    # @property
    # def emailAddr(self):
    #     return self._email    
    #     
    # @emailAddr.setter
    # def emailAddr(self, emailAddr):
    #     self._email = emailAddr
    # 
    # # ----- Surname -----
    # @property
    # def surname(self):
    #     return self._surname  
    # 
    # @surname.setter
    # def surname(self, surname):
    #     self._surname = surname
    # 
    # # ----- Firstname -----  
    # @property
    # def firstname(self):
    #     return self._firstname
    # 
    # @firstname.setter
    # def firstname(self, firstname):
    #     self._firstname = firstname
    # 
    #  # ----- Date of birth -----        
    # @property
    # def dob(self):
    #     return self._dob
    # 
    # @dob.setter    
    # def dob(self, dob):
    #     self._dob = dob
    # 
    # # ----- Gender -----    
    # @property
    # def gender(self):
    #     return self._gender
    # 
    # @gender.setter    
    # def gender(self, gender):
    #     self._gender = gender
    #     
    # # ----- Phone number ------        
    # @property
    # def phone(self):
    #     return self._phone
    # 
    # @phone.setter    
    # def phone(self, phone):
    #     self._phone = phone
    # 
    # # ----- Country Code -----    
    # @property
    # def countryCode(self):
    #     return self._countryCode
    # 
    # @countryCode.setter    
    # def countryCode(self, countryCode):
    #     self._countryCode = countryCode
    # 
    # # ----- lastBooking -----        
    # @property
    # def lastBooking(self):
    #     return self._lastBooking
    # 
    # # ----- total Bookings -----        
    # @property
    # def totalBookings(self):
    #     return self._totalBookings
  
    # ----- any error codes -----  
    @property
    def error(self):
        return self._error 
  
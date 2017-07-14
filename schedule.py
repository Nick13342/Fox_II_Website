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
    def __setSchedule(self,row):
        # Allocate the retrieved columns into the object variables.
        self._CruiseDate = row['CruiseDate']
        self._CruiseNo = row['CruiseNo']
        self._departure = row['departure']
        self._BoatID = row['BoatID']
        self._RouteID = row['RouteID']
        self._return = row['return']
        self._available = row['available']
        self._status = row['status']

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
    def readSched(self, con, CruiseDate, CruiseNo):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        
        # Check the date is in the correct format.  The query would fail to return a record anyway
        # but it's nicer to return to the calling program a valid reason why it has failed.
        if not self.__validateDT(CruiseDate, "%Y-%m-%d"):
            self._error = "Invalid date format"
            self._retvalue = False
            return self._retvalue
       
        # Like the date, a cruise number has to be greater than 0 so we will check it here as well 
        if CruiseNo < 1:
            self._error = "Cruise Number must be greater than 0"
            self._retvalue = False
            return self._retvalue               
        
        # define SQL query
        read_query = "select * from schedule where CruiseDate = ? and CruiseNo = ?"
       
        try:
            # define cursone and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query, (CruiseDate, CruiseNo))
        
            row = cur.fetchone();
            
            if row == None:
                self._error = "No schedule record found for date " + str(CruiseDate) + " and number  " + str(CruiseNo)
                self._retvalue = False
            else:
                self.__setCustomer(row)
    
            
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
            
        return (self._retvalue, row)
    
    #-----------------------------------------------------------------------------------------------
    # Read the schedule record and return those matching the starting and ending dates as passed
    # from the calling program
    #-----------------------------------------------------------------------------------------------
    def readSchedulebyDate(self, con, startDate, endDate):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        rows = None
        
        # Check that the dates are in a valid format and consistant with those that will be stored
        # within the Schedule table
        if not self.__validateDT(startDate, "%Y-%m-%d") or not self.__validateDate(endDate, "%Y-%m-%d") :
            self._error = "Invalid date format"
            self._retvalue = False
            return (self._retvalue, rows)
        
        if startDate > endDate:
            self._error = "Start date cannot be greater than end date"
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
    # Insert a new schedule using the property values for schedule which need to have been
    # set by the calling program.
    #-------------------------------------------------------------------------------------------------
    def insertSchedule(self, con):
        # retValue contains the success or failure of the update operation. Default to success
        self._retvalue = True
        self._error = None
        
        # Do any data validation checks here to ensure database integrity.  Some fields will be handled by
        # constraints within the database itself.  
        if not self.__validateDT(self._CruiseDate, "%Y-%m-%d"):
            self._error = "Invalid date format"
            self._retvalue = False
            return self._retvalue
    
        # Check the departure time is the time format we require
        if not self.__validateDT(self._departure, "%H:%M"):
            self._error = "Invalid departure time format"
            self._retvalue = False
            return self._retvalue
       
        # Check the return time is the time we require          
        if not self.__validateDT(self._return, "%H:%M"):
            self._error = "Invalid return time format"
            self._retvalue = False
            return self._retvalue

        # Even though the CruiseNo field is defined as Integer, SQLite will allow string values
        # to be inserted! So doesn't hurt to to a check here. 
        if not str.isdigit(self._CruiseNo):
            self._error = "CruiseNo is not numeric"
            self._retvalue = False
            return self._retvalue          
        
        # define SQL query
        insert_query = "insert into schedule (CruiseDate, CruiseNo, departure, BoatID, RouteID, \
        return, available, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)" 
    
        # attempt to execute the query        
        try:
            cur = con.cursor()
        
            cur.execute(insert_query, (self._Cruisedate, self._CruiseNo, self._departure, \
                                self._BoatID, self._RouteID, self._return, self._available, \
                                self._status))        
        
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
    
    # ----- Cruise Date ------
    @property
    def CruiseDate(self):
        return self._CruiseDate
    
    @CruiseDate.setter
    def CruiseDate(self, CruiseDate):
        self._CruiseDate = CruiseDate 
   
    # ----- Cruise Date ------
    @property
    def CruiseNo(self):
        return self._CruiseNo
    
    @CruiseNo.setter
    def CruiseNo(self, CruiseNo):
        self._CruiseNo = CruiseNo 
    
    
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
  
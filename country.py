import sqlite3

#------------------------------------------------------------------------------------
# Class Name: Country
# Written By: Nick Glanville
# Date:       26-07-2017
#
# Class to create allow an instance of an Country object.  This class is designed to
# perform all of the basic database functions on the Country table. 
#------------------------------------------------------------------------------------

class Country:
    
   
    #---------------------------------------------------------------------------------
    # Initialise instance of country
    #---------------------------------------------------------------------------------
    def __init__(self):      
        pass  
  
    #-----------------------------------------------------------------------------------------------
    # Read a country by Code
    #-----------------------------------------------------------------------------------------------  
    def readCountryByCode(self, con, countryCode):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        country = ""
        
        # define SQL query
        read_query = "SELECT c.country \
                     FROM country c \
                     WHERE c.countryCode = ?"
        
        try:
            # define curson and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query,(countryCode.upper(),))
        
            rows = cur.fetchall();
            
            if not rows:
                self._error = "No Country records found for country code: "+ countryCode.upper()
                self._retvalue = False
            else:
                country = rows[0]['country']
       
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
        
        # return the country name    
        return (self._retvalue, country)
    
  
  
    #-----------------------------------------------------------------------------------------------
    # Read all countries from the country table
    #-----------------------------------------------------------------------------------------------  
    def readCountries(self, con):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        rows = []
        
        # define SQL query
        read_query = "SELECT c.CountryCode, c.country \
                     FROM country c \
                     ORDER by country"
        
        try:
            # define cursone and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query)
        
            rows = cur.fetchall();
            
            if not rows:
                self._error = "No Country records found"
                self._retvalue = False
       
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
            
        return (self._retvalue, rows)
    
     
    # ----- any error codes -----  
    @property
    def error(self):
        return self._error 
import sqlite3
from debug import Debug

#------------------------------------------------------------------------------------
# Class Name: Route
# Written By: Nick Glanville
# Date:       07-09-2017
#
# Class to create allow an instance of an Route object.  This class is designed to
# perform all of the basic database functions on the route table. 
#------------------------------------------------------------------------------------

class Route:
    
    #---------------------------------------------------------------------------------
    # Initialise instance of country
    #---------------------------------------------------------------------------------
    def __init__(self):      
        self._db = Debug("country",False)  
  
    #-----------------------------------------------------------------------------------------------
    # Read a country by Code
    #-----------------------------------------------------------------------------------------------  
    def readRouteByID(self, con, RouteID):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        rows = []
        
        # define SQL query
        read_query = "SELECT r.description, r.duration, r.costPPA, r.costPPC \
                     FROM route r \
                     WHERE r.RouteID = ?"
        
        try:
            # define curson and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query,(RouteID,))
        
            rows = cur.fetchall();
            
            if not rows:
                self._error = "No Routes found for ID: "+ RouteID()
                self._retvalue = False
   
       
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
        
        # return the country name    
        return (self._retvalue, rows)
    
  
  
    #-----------------------------------------------------------------------------------------------
    # Read all routes from the route table
    #-----------------------------------------------------------------------------------------------  
    def readRoutes(self, con):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        rows = []
        
        # define SQL query
        read_query = "SELECT r.RouteID, r.description \
                     FROM route r \
                     ORDER by r.RouteID"
        
        try:
            # define cursone and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query)
        
            rows = cur.fetchall();
            
            if not rows:
                self._error = "No Route records found"
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
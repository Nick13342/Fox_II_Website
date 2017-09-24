import sqlite3
from debug import Debug

#------------------------------------------------------------------------------------
# Class Name: Boat
# Written By: Nick Glanville
# Date:       07-09-2017
#
# Class to create allow an instance of an Boat object.  This class is designed to
# perform all of the basic database functions on the boat table. 
#------------------------------------------------------------------------------------

class Boat:
    
   
    #---------------------------------------------------------------------------------
    # Initialise instance of country
    #---------------------------------------------------------------------------------
    def __init__(self):
        self._db = Debug("country",False)
  
    #---------------------------------------------------------------------------------
    #  Internal function to set the property values to the current row.  The __ at the
    #  start of the dunction indicate that it cannot be access for any calling programs
    #---------------------------------------------------------------------------------     
    def __setBoat(self,row):
        # Allocate the retrieved columns into the object variables.
        self._BoatID = row['BoatID']
        self._name = row['name']
        self._description = row['description']
        try:
            self._length = float(row['length'])
        except:
            self._length = None
        try:
            self._beam = float(row['beam'])
        except:
            self._beam = None
        try:
            self._draught = float(row['draught'])
        except:
            self._draught = None
        try:    
            self._capacity = int(row['capacity'])
        except:
            self._capacity = None
  
    #-----------------------------------------------------------------------------------------------
    # Read a Boat by Code
    #-----------------------------------------------------------------------------------------------  
    def readBoatByID(self, con, BoatID):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        rows = []
        
        # define SQL query
        read_query = "SELECT b.BoatID, b.name, b.description, b.length, b.beam, b.draught, b.capacity \
                     FROM boat b \
                     WHERE b.BoatID = ?"
        
        try:
            # define curson and execute the query, BoatID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query,(BoatID,))
        
            rows = cur.fetchall();
            
            if not rows:
                self._error = "No Boat found for ID: "+ BoatID
                self._retvalue = False
            else:
                self.__setBoat(rows[0])
       
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
        
        # return the country name    
        return (self._retvalue, rows)
    
  
  
    #-----------------------------------------------------------------------------------------------
    # Read all boats from the boat table
    #-----------------------------------------------------------------------------------------------  
    def readBoats(self, con):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = True
        self._error = None
        rows = []
        
        # define SQL query
        read_query = "SELECT b.BoatID, b.name \
                     FROM boat b \
                     ORDER by b.name"
        
        try:
            # define cursone and execute the query, CustID is the primary key so we will only expect
            # one record to be returned.
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(read_query)
        
            rows = cur.fetchall();
            
            if not rows:
                self._error = "No Boat records found"
                self._retvalue = False
       
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            self._retvalue = False
            
        return (self._retvalue, rows)
    
  
# Property funmctions here  
    @property
    def BoatID(self):
        return self._BoatID
  
    @property
    def name(self):
        return self._name  
 
    @property
    def description(self):
        return self._description
    
    @property
    def length(self):
        return self._length 
    @property
    def beam(self):
        return self._beam
    
    @property
    def drought(self):
        return self._draught
    
    @property
    def capacity(self):
        return self._capacity
        
    
    # ----- any error codes -----  
    @property
    def error(self):
        return self._error 
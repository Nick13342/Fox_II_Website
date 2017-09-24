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

class Login:
    
   
    #---------------------------------------------------------------------------------
    # Initialise instance of admin
    #---------------------------------------------------------------------------------
    def __init__(self):
        self._db = Debug("admin",True)
  
    #-----------------------------------------------------------------------------------------------
    # Read a Boat by Code
    #-----------------------------------------------------------------------------------------------  
    def AuthLoginByUserCode(self, con, UserCode, password):
        # retValue contains the success or failure of the read operation. Default to success
        self._retvalue = False
        self._error = None
        
        self._db.print(self._retvalue)
        
        # define SQL query
        query = "SELECT u.Password FROM users u WHERE u.UserCode = ?"
        
        self._db.print(query)
        
        try:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(query, (UserCode,))
            
            self._db.print("Execute")
            
            row = cur.fetchone();
            
            
            
            if row == None:
                self._error = "No User found for User Code: "+ UserCode
                self._db.print(self._error) 
                self._retvalue = False
                return (self._retvalue, self._error)
            
            self._db.print(row[0])
            self._db.print(password)            
            
            if row[0] == password:
                self._db.print("If")
                self._retvalue = True
            
            else:
                self._error = "Incorrect Password"
                self._db.print("else")
                self._retvalue = False
                return (self._retvalue, self._error)
       
        # Exception processing logic here.            
        except Exception as err:
            self._error = "Query Failed: " + str(err)
            
            self._db.print(self._error)
            
        return (self._retvalue)
    
  
# Property functions here  
    @property
    def UserCode(self):
        return self.UserCode
  
    @property
    def password(self):
        return self.password
    
    # ----- any error codes -----  
    @property
    def error(self):
        return self._error 
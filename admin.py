import sqlite3

#------------------------------------------------------------------------------------
# Class Name: Login
# Written By: Nick Glanville
# Date:       26-07-2017
#------------------------------------------------------------------------------------

class Login:
    
   
    #---------------------------------------------------------------------------------
    # Initialise instance of login
    #---------------------------------------------------------------------------------
    def __init__(self):      
        pass
        
    #---------------------------------------------------------------------------------
    # Stuff
    #---------------------------------------------------------------------------------
    
    def confirmUsername(self, username, dbUsername):
        if self.username == dbUsername:
            return(True)
        else:
            return(False)
        
    def confirmPassword(self, password, dbPassword):
        if self.password == dbPassword:
            return(True)
        else:
            return(False)    
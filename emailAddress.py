#!/usr/bin/env python3
from debug import Debug

#------------------------------------------------------------------------------------
# Class Name: email
# Written By: Nick Glanville
# Date:       03-07-2017
#
# Class to create an instance of an email object.  At this stage the primary
# function of the class is to validate the email address, but other functionality
# related to an email can be added.
#------------------------------------------------------------------------------------

class Email:
   
    #----------------------------------------------------------------------------------
    # Maintain a list of common incorrect domain names here as class variables so they
    # are consistant across all instances of the object
    #----------------------------------------------------------------------------------
    domains = []
    domains.append("extra.co.nz")
    domains.append("extra.com")
    domains.append("xtra.com")
    domains.append("gmail.co.nz")
    domains.append("gmail.nz")
    domains.append("google.co.nz")
    
  
    #----------------------------------------------------------------------------------
    # Initilise the object with email address and assume that it's a valid email
    #----------------------------------------------------------------------------------
    def __init__(self, NewEmail):
        #set debugging
        self._db = Debug("email",False)
        self._emailAddress = NewEmail
  
    #----------------------------------------------------------------------------------
    # Method here to check the email address
    # Several checks are made and the method returns immediately there is a failed
    # check.  Other checks may be added to tigten up on invalid emails when required
    #----------------------------------------------------------------------------------  
    def validEmailAddress(self):
        self._error = ""
      
        # Blank is not a valid email address  
        if not self._emailAddress:
            self._error = "Email address is blank"
            return(False)
        
        # Email addresses must contain an @ symbol
        if '@' not in self._emailAddress:
            self._error = "Email address does not contain @"
            return(False)
        
        # Cannot start with an @ or a . character
        if self._emailAddress[0] == '@' or self._emailAddress[0] == '.':
            self._error = "Email address cannot begin with @ or ."   
            return(False)
        
        # Cannot finish with an @ or a . character     
        if self._emailAddress[-1:] == '@' or self._emailAddress[-1:] == '.':
            self._error = "Email address cannot end with @ or ."   
            return(False)
        
        # Now lets split the email address on the @ symbol for more checking   
        self._emailParts = self._emailAddress.split('@')
        
        # Cannot have multiple @ symbols 
        if len(self._emailParts) > 2:
           self._error = "Email address cannot have multiple @ characters"   
           return(False)
        
        # cannot have a . either side of a @ system
        if self._emailParts[0][-1:] == '.' or self._emailParts[1][0] == '.':
            self._error = "Email address cannot have a . immediately before or after the @"
            return(False)
        
        # Must have a '.' in the second part of the email
        if '.' not in self._emailParts[1]:
            self._error = "Email address must contain a . after the @ symbol"   
            return(False)    

        # Lets now check against some commom mistaken domain names
        for self._domain in Email.domains:
            if self._emailParts[1].lower() == self._domain:
               self._error = "Invalid domain name: " + self._emailParts[1].lower()
               return(False)
        
        # if we have got this far we will call it a valid email address
        return(True)    
                
  #---------------------------------------------------------------------------------
  #  Define getter and setter routines here.
  #---------------------------------------------------------------------------------
 
  # Allow calling program to interrogate the error code  
    @property
    def error(self):
        return self._error
    
 
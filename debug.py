#!/usr/bin/env python3

#------------------------------------------------------------------------------------
# Class Name: debug
# Written By: Nick Glanville
# Date:       10-07-2017
#
# Class to create an instance of an debug object.  This can be called and turned
# on from any module to trace problems
#------------------------------------------------------------------------------------

from datetime import datetime

class Debug:
    
   
    #----------------------------------------------------------------------------------
    # Initilise the object with a flag True or False to see if enabled
    #----------------------------------------------------------------------------------
    def __init__(self, ModuleName, Enabled):
        self._enabled = Enabled
        self._moduleName = ModuleName
  
    #----------------------------------------------------------------------------------
    # Method here to print what has been sent to it
    #----------------------------------------------------------------------------------  
    def print(self, printString):
        
        if not self._enabled:
            return
   
        today = datetime.now().strftime("%Y-%m-%d %H:%M")                 
        print("%s: %s - %s" % (self._moduleName, today, printString))

        return    
           
    #-----------------------------------------------------------------------------------
    # Allow debugging to be turned on or off as we go by setting the enabled property
    #-----------------------------------------------------------------------------------

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, enabled):
        self._enabled = enabled    
 
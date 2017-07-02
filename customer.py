import sqlite3

class Customer:
    
    def __init__(self):
        self.__surname = ""
        self.__firstname = ""
        self.__email = ""
        self.__dob = ""
        self.__gender = ""
        self.__phone = ""
        self.__countryCode = ""
        self.__lastBooking = ""
        self.__totalBookings = ""
        
    def readCust(self, con, CustID):
        read_query = "select * from customer where CustID = ?"
        
        con.row_factory = sqlite3.Row
        
        cur = con.cursor()
        cur.execute(read_query, (CustID,))
        
        row = cur.fetchone();
        
        self.__email = row['Email']
        self.__surname = row['surname']
        self.__firstname = row['firstname']
        self.__dob = row['D.O.B']
        self.__gender = row['gender']
        self.__phone = row['phone']
        self.__countryCode = row['CountryCode']
        self.__lastBooking = row['lastBooking']
        self.__totalBookings = row['totalBookings']        
    
    def updateCust(self, con, CustID):
        self.__retvalue = True
        #update_query = "update customer set Email = ?, surname = ?," \
        #"firstname = ?, D.O.B = ?, gender = ?, phone = ?, CountryCode = ?," \
        #"lastBooking = ?, totalBookings = ? where CustID = ?"
        
        update_query = "update customer set Email = ?, surname = ?," \
        "firstname = ?, D.O.B = ?, gender = ?, phone = ?, CountryCode = ? where CustID = ?"        
        
        #con.row_factory = sqlite3.Row
        try:
            cur = con.cursor()
            cur.execute(update_query, (self.__email, self.__surname, self.__firstname, \
                                       None, self.__gender, self.__phone, self.__countryCode, CustID))
        
        #cur.execute(update_query, (self.__email, self.__surname, self.__firstname, \
                                #self.__dob, self.__gender, self.__phone, self.__countryCode, \
                                #self.__lastBooking, self.__totalBookings, CustID))        
        
            con.commit()
        except:
            self.retvalue = False
        
        return self.__retvalue
    
    
    @property
    def emailAddr(self):
        return self.__email    
        
    @emailAddr.setter
    def emailAddr(self, emailAddr):
        self.__email = emailAddr
    
    
    
    @property
    def surname(self):
        return self.__surname  
    
    @surname.setter
    def surname(self, surname):
        self.__email = surname
      
    
    
    @property
    def firstname(self):
        return self.__firstname
    
    @firstname.setter
    def firstname(self, firstname):
        self.__email = firstname
        
        
    
    @property
    def dob(self):
        return self.__dob
    
    @dob.setter    
    def dob(self, dob):
        self.__email = dob
        
        
        
    @property
    def gender(self):
        return self.__gender
    
    @gender.setter    
    def gender(self, gender):
        self.__email = gender
        
        
        
    @property
    def phone(self):
        return self.__phone
    
    @phone.setter    
    def phone(self, phone):
        self.__email = phone
    
    
    
    @property
    def countryCode(self):
        return self.__countryCode
    
    @countryCode.setter    
    def countryCode(self, countryCode):
        self.__email = countryCode
        
        
        
    @property
    def lastBooking(self):
        return self.__lastBooking
    
    @lastBooking.setter    
    def lastBooking(self, lastBooking):
        self.__email = lastBooking
        
        
        
    @property
    def totalBookings(self):
        return self.__totalBookings
    
    @totalBookings.setter    
    def totalBookings(self, totalBookings):
        self.__email = totalBookings
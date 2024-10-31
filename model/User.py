class User: #Creating a User class
    
    def __init__(self, firstName, lastName, userEmail, userPassword, userAdress, userPhone, isAdmin=None):
        
        #Initialising all the parameters
        self.firsName = firstName
        self.lastName = lastName
        self.userEmail = userEmail
        self.userAdress = userAdress
        self.userPhone = userPhone
        self.userPassword = userPassword
        
        #Checking if the isAdmin parameter has a variable
        if isAdmin is not None:
            self.isAdmin = isAdmin
        else:
            self.isAdmin = False
            
        
    
            
    
        
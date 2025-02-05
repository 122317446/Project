class User: #Creating a User class
    
    def __init__(self, userID, firstName, lastName, userEmail, userPassword, userAdress, userPhone, isAdmin=None):
        
        #Initialising all the parameters
        self.userID = userID
        self.firstName = firstName
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

    def to_dict(self):
        return {
            "userID": self.userID,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "userEmail": self.userEmail,
            "userPassword": self.userPassword,
            "userAdress": self.userAdress,
            "userPhone": self.userPhone,
            "isAdmin": self.isAdmin,
        }

from dao.UserDAO import UserDAO
from model.User import User
from validation.UserValidation import UserValidation

class UserService:
    
    def __init__(self):
        
        #Create an instance of UserDAO to handle user data
        self.userDAO = UserDAO()
        self.userValidation = UserValidation()
        
    def get_all_users(self):
        return self.userDAO.getAllUsers()
    
    
    def login(self, email, password): #Creating login function
        
        #Retrieve the list of all users from UserDAO
        userlistToCheckAgainst = self.userDAO.getAllUsers()
        
        #Flag to check if the user is found
        user_found = False
        
        #Iterate through the list of users to find a matching user
        for user in userlistToCheckAgainst:
            if user.userEmail == email and user.userPassword == password:
                user_found = True
                if user.isAdmin:
                    return True
                else:
                    return False
        
        return None
             
          
    def signUp(self, firstName, lastName, userEmail, userPassword, userAdress, userPhone):
        
        if (self.userValidation.checkEmail(self.userDAO.getAllUsers(), userEmail)
            and self.userValidation.checkPassword(userPassword)):
            
            idcount = len(self.get_all_users()) + 1 
            
            userToCreate = User(idcount, firstName, lastName, userEmail, userPassword, userAdress, userPhone, isAdmin=None)
            self.userDAO.createUser(userToCreate)
            return True
            #Redirect user to homepage with the newly created account
        else:
            #Alert or prompt user that account creation has failed
            return False
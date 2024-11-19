from dao.UserDAO import UserDAO
from model.User import User

class UserService:
    
    def __init__(self):
        
        #Create an instance of UserDAO to handle user data
        self.userDAO = UserDAO()
        '''self.userValidation = UserValidation'''
        
    
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
            else:
                #If no matching user is found, display an error message
                if user_found == False:
                    #Alert or prompt user account is not found
                    return None
                
            
    def signUp(self, firstname, lastname, email, address, phone, password):
        
        if (self.userValidation.checkEmail(self.userDAO.getAllUsers(), email)
            and self.userValidation.checkPassword(password)):
            
            userToCreate = User(firstname, lastname, email, address, phone, password)
            self.userDAO.createUser(userToCreate)
            #Redirect user to homepage with the newly created account
        else:
            #Alert or prompt user that account creation has failed
            self.signUp() #Recursive call 
            
        
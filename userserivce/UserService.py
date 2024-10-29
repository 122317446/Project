from userdao.UserDAO import UserDAO
from model.User import User

class UserService:
    
    def __init__(self, UserValidation):
        
        #Create an instance of UserDAO to handle user data
        self.userDAO = UserDAO([])
        self.userValidation = UserValidation
        
    
    def login(self): #Creating login function
        
        #Retrieve the list of all users from UserDAO
        userlistToCheckAgainst = self.userDAO.getAllUsers()
        
        #Promt the user for email and password input
        email = input("Enter your Email: ")
        password = input("Enter your password: ")
        

        #Flag to check if the user is found
        user_found = False
        
        #Iterate through the list of users to find a matching user
        for user in userlistToCheckAgainst:
            if user.userEmail == email and user.userPassword == password:
                user_found = True
                if user.isManager:
                    print("Hello Manager, Welcome back")
                else:
                    print("Hello Employee, Welcome back")
                break #Exit the loop once the user is found
        
        #If no matching user is found, display an error message
        if not user_found:
            print("Invalid username or password. Try again.")
            self.login()
            
    def signUp(self):
        firstName = input("Enter first name: ")
        lastName = input("Enter last name: ")
        email = input("Enter Email: ")
        password = input("Enter password: ")
        
        if (self.userValidation.checkEmail(self.userDAO.getAllUsers(), email)
            and self.userValidation.checkPassword(password)):
            
            userToCreate = User(firstName, lastName, email, password)
            self.userDAO.createUser(userToCreate)
            print(f"Hello {firstName} {lastName}, your account has been created successfully")
            for user in self.userDAO.getAllUsers():
                print(user)
        else:
            print("Sign up failed. Please try again")
            self.signUp() #Recursive call 
            
        
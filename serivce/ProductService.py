from dao.ProductDAO import ProductDAO
from model.Product import Product

class ProductService:
    
    def __init__(self, ProductValidation):
        
        #Create an instance of ProductDAO to handle user data
        self.ProductDAO = ProductDAO([])
        self.ProductValidation = ProductValidation
        
    
    def fetchproducts(self): #
        
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
            
        
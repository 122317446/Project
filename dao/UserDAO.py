from model.User import User

class UserDAO:
    
    def __init__(self, user_list=None):
        #Initialise user_list as an empty list if None is provided
        self.user_list = user_list if user_list is not None else []
        
    #This method grabs all users, and creates some if the list is empty
    def getAllUsers(self):
        if not self.user_list: #Check if the list is empty
            #Create default users if list is empty
            user_admin = User(1, 'K', 'C', 'kc@gmail.com', '12345', 'IE', 0000, True)
            
            self.user_list.append(user_admin)           
        return self.user_list
    
    #Add a new user to the list
    def createUser(self, user):
        self.user_list.append(user)
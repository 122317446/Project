from dao.UserDAO import UserDAO
from validation.UserValidation import UserValidation
from model.User import User

class UserService:
    def __init__(self):
        self.userDAO = UserDAO()
        self.userValidation = UserValidation()

    def get_all_users(self):
        return self.userDAO.get_all_users()

    def login(self, email, password):
        user = self.userDAO.get_user_by_email(email)
        if user and user.userPassword == password:
            return user  # True for admin, False for customer
        return None

    def signUp(self, firstName, lastName, userEmail, userPassword, userAdress, userPhone):
        if (self.userValidation.checkEmail(self.userDAO.get_all_users(), userEmail) and
                self.userValidation.checkPassword(userPassword)):
            
            # Create a user object without specifying userID
            userToCreate = User(None, firstName, lastName, userEmail, userPassword, userAdress, userPhone, isAdmin=False)
            self.userDAO.add_user(userToCreate)
            return True
        return False
    
    def update_user(self, user):
        # Validate input or any additional logic here if needed
        self.userDAO.update_user(user)



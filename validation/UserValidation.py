import re

class UserValidation:
    def __init__(self):
        pass
    
    def checkEmail(userlist, email):
        if "@" not in email or "." not in email: #Not too important
            print("Email doesn't have the key characters '@' and '.'.")
            return False
        
        for user in userlist: #More important
            if user.userEmail == email:
                print("Email already has an account")
                return False
            
        return True
    
    def checkPassword(password):
        pattern = re.compile(r'[^a-zA-Z0-9]') #Use chatGPT to create a character check 
        if len(password) < 10:
            print("Password must be at least 10 characters long")
            return False
        if not pattern.search(password):
            print("Password must contain at least one special character")
            return False
        return True
        #If you want you can add another validation asking user to type the password again
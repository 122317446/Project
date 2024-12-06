import re

class UserValidation: #This validation class will be used to create barriers and security measueres when creating an account
    def __init__(self):
        pass
    
    def checkEmail(self, userlist, email):
        if "@" not in email or "." not in email: 
            return False
        
        for user in userlist:
            if user.userEmail == email:
                return '0'
            
        return True
    
    def checkPassword(self, password):
        pattern = re.compile(r'[^a-zA-Z0-9]') #Use chatGPT to create a character check 
        if len(password) < 10:
            return False
        else:
            if pattern.search(password):
                return True
            else:
                return False
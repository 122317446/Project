import sqlite3
from model.User import User

class UserDAO:
    def __init__(self, db_name="website.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        # Create the User table if it doesn't already exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                userID INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                userEmail TEXT UNIQUE NOT NULL,
                userPassword TEXT NOT NULL,
                userAdress TEXT NOT NULL,
                userPhone TEXT NOT NULL,
                isAdmin INTEGER DEFAULT 0
            )
        ''')
        self.connection.commit()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM User")
        rows = self.cursor.fetchall()
        return [User(row['userID'], row['firstName'], row['lastName'], row['userEmail'], row['userPassword'], row['userAdress'], row['userPhone'], bool(row['isAdmin'])) for row in rows]

    def get_user_by_id(self, userID):
        self.cursor.execute("SELECT * FROM User WHERE userID = ?", (userID,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        return None
    
    def get_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM User WHERE userEmail = ?", (email,))
        row = self.cursor.fetchone()
        if row:
            return User(row['userID'], row['firstName'], row['lastName'], row['userEmail'], row['userPassword'], row['userAdress'], row['userPhone'], bool(row['isAdmin']))
        return None

    def add_user(self, user):
        self.cursor.execute(
            '''
            INSERT INTO User (firstName, lastName, userEmail, userPassword, userAdress, userPhone, isAdmin)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                user.firstName,
                user.lastName,
                user.userEmail,
                user.userPassword,
                user.userAdress,
                user.userPhone,
                int(user.isAdmin)
            )
        )
        self.connection.commit()
        
    def delete_user(self, userID):
        self.cursor.execute("DELETE FROM User WHERE userID = ?", (userID,))
        self.connection.commit()
    
    def update_user(self, user):
        self.cursor.execute(
            '''
            UPDATE User
            SET firstName = ?, 
                lastName = ?, 
                userEmail = ?, 
                userPassword = ?, 
                userAdress = ?, 
                userPhone = ?, 
                isAdmin = ?
            WHERE userID = ?
            ''',
            (
                user.firstName,
                user.lastName,
                user.userEmail,
                user.userPassword,
                user.userAdress,
                user.userPhone,
                int(user.isAdmin),  # Convert bool to integer for the database
                user.userID
            )
        )
        self.connection.commit()



    def close_connection(self):
        self.connection.close()

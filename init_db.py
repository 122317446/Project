from dao.UserDAO import UserDAO
from dao.ProductDAO import ProductDAO

def initialize_database():
    # Initialize both DAOs to create their tables in website.db
    user_dao = UserDAO(db_name="website.db")
    product_dao = ProductDAO(db_name="website.db")
    
    print("Database initialized! Both Product and User tables created in website.db.")
    
    # Close connections
    user_dao.close_connection()
    product_dao.close_connection()

if __name__ == "__main__":
    initialize_database()

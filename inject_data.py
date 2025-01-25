from dao.ProductDAO import ProductDAO
from dao.UserDAO import UserDAO
from model.Product import Product
from model.User import User

def initialize_database():
    product_dao = ProductDAO(db_name="website.db")
    user_dao = UserDAO(db_name="website.db")
    print("Database initialized! Both Product and User tables created.")
    product_dao.close_connection()
    user_dao.close_connection()

def inject_sample_data():
    # Inject product data
    product_dao = ProductDAO(db_name="website.db")

    sample_products = [
        Product(None, 'Phillips Screwdriver', 'Handy screwdriver', 12, 50, 'Hand-tool', ['Carbon-fibre', 'Excellent grip', 'Ratchet'], "A_Phillips_screwdriver_with_a_metallic_handle_and_.png"),
        Product(None, 'Dallas Mini-Driver', 'A small driver', 80, 40, 'Hand-tool', ['Modular', 'Made-in Dallas', 'Cordless'], "A_small_handheld_driver_called_Dallas_Mini-Driver,.png"),
        Product(None, 'Pickaxe', 'Minecraft themed pickaxe', 100, 10, 'Merchandise', ['Merch', 'Kid-friendly', 'Great gift'], "A_Minecraft-themed_pickaxe_with_a_stylized,_pixela.png"),
        Product(None, 'TAC Excavator', 'Excavator with a crush power rated 9000', 10000, 12, 'Machinery', ['Non-modular', 'Safety: A', 'Transportable'], "A_powerful_excavator_with_a_rugged_design,_labeled.png"),
        Product(None, 'Safety Helmet', 'Yellow safety helmet', 5, 30, 'Equipment', ['Light', 'Strong', 'Strapless'], "A_yellow_safety_helmet_with_a_strong_build_and_a_s.png"),
        Product(None, 'TAC Drill Rig', 'Drill Rig capable of mining minerals like oil', 350000, 45, 'Machinery', ['Sturdy', 'Non-portable', '1000tonne limit'], "A_TAC_Drill_Rig_with_a_sturdy_structure,_capable_o.png"),
        Product(None, 'Safety boots', 'Boots with good tread and traction', 50, 80, 'Equipment', ['Heavyduty', 'Fits all', 'Aggressive treading'], "A_pair_of_rugged_safety_boots_with_deep_tread_and_.png"),
        Product(None, 'TAC Power generator', '2000W portable generator', 450, 100, 'Electrical', ['Light-weight', 'Portable','Energy: B+'], "A_portable_TAC_Power_generator_with_a_2000W_capaci.png"),
    ]

    for product in sample_products:
        try:
            product_dao.add_product(product)
            print(f"Added product: {product.prodName}")
        except Exception as e:
            print(f"Error adding product: {e}")
    
    product_dao.close_connection()

    # Inject user data
    user_dao = UserDAO(db_name="website.db")

    sample_users = [
        User(None, 'K', 'C', 'kc@gmail.com', '12345', 'IE', '0000', True),  # Admin
        User(None, 'Jane', 'Doe', 'jane@gmail.com', '54321', 'US', '1111', False)  # Regular user
    ]

    for user in sample_users:
        try:
            user_dao.add_user(user)
            print(f"Added user: {user.userEmail}")
        except Exception as e:
            print(f"Error adding user: {e}")
    
    user_dao.close_connection()

if __name__ == "__main__":
    initialize_database()  # Ensure tables are created
    inject_sample_data()   # Inject sample data

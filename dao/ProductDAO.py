from model.Product import Product

class ProductDAO:
           
    def __init__(self):
        
        self.products = [
            #Creating the product data
            Product(1, 'Phillips Screwdriver', 'Handy screwdriver', 12, 50, 
                    ['Carbon-fibre', 'Excellent grip', 'Ratchet'], "A_Phillips_screwdriver_with_a_metallic_handle_and_.png"),
            Product(2, 'Dallas Mini-Driver', 'A small driver', 80, 40, 
                    ['Modular', 'Made-in Dallas', 'Cordless'], "A_small_handheld_driver_called_Dallas_Mini-Driver,.png"),
            Product(3, 'Pickaxe', 'Minecraft themed pickaxe', 100, 10, 
                    ['Merch', 'Kid-friendly', 'Great gift'], "A_Minecraft-themed_pickaxe_with_a_stylized,_pixela.png"),
            Product(4, 'TAC Excavator', 'Excavator with a crush power rated 9000', 10000, 12, 
                    ['Non-modular', 'Safety: A', 'Transportable'], "A_powerful_excavator_with_a_rugged_design,_labeled.png"),
            Product(5, 'Safety Helmet', 'Yellow safety helmet', 5, 30, 
                    ['Light', 'Strong', 'Strapless'], "A_yellow_safety_helmet_with_a_strong_build_and_a_s.png"),
            Product(6, 'TAC Drill Rig', 'Drill Rig capable of mining minerals like oil', 350000, 45, 
                    ['Sturdy', 'Non-portable', '1000tonne limit'], "A_TAC_Drill_Rig_with_a_sturdy_structure,_capable_o.png"),
            Product(7, 'Safety boots', 'Boots with good tread and traction', 50, 80, 
                    ['Heavyduty', 'Fits all', 'Aggressive treading'], "A_pair_of_rugged_safety_boots_with_deep_tread_and_.png"),
            Product(8, 'TAC Power generator', '2000W portable generator', 450, 100, 
                    ['Light-weight', 'Portable','Energy: B+'], "A_portable_TAC_Power_generator_with_a_2000W_capaci.png")
        ]
    
    #Fucntions to pull all / certain data
    def getAllProducts(self):
        return self.products
    
    def getProductbyID(self, prodID):
        for product in self.products:
            if product.prodID == prodID:
                return product
        return None

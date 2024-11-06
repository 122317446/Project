from model.Product import Product

class ProductDAO:
           
    def __init__(self):
        
        self.products = [
            #Creating the product list
            Product(1, 'Phillips Screwdriver', 'A screwdriver', 12, 50, 5),
            Product(2, 'Milwaukee Mini-Driver', 'A small driver', 80, 40, 2),
            Product(3, 'Pickaxe', 'Minecraft themed pickaxe', 100, 10, 1),
            Product(4, 'Shovel', 'Minecraft themed shovel', 100, 12, 1),
            Product(5, 'Safety Helmet', 'Yellow safety helmet', 5, 30, 0),
            Product(6, 'Sledgehammer', '100kg sledgehammer', 35, 45, 1),
            Product(7, 'Safety boots', 'Boots with good tread and traction', 50, 80, 0),
            Product(8, 'Power generator', '100W portable generator', 200, 100, 5)
        ]

    def getAllProducts(self):
        return self.products
    
    def getProductbyID(self, prodID):
        for product in self.products:
            if product.prodID == prodID:
                return product
        return None

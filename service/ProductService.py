from dao.ProductDAO import ProductDAO
from model.Product import Product

class ProductService:
    
    def __init__(self):
        self.product_dao = ProductDAO()
        
    def get_all_products(self):
        return self.product_dao.getAllProducts()
    
    def get_product_details(self, prodID):
        return self.product_dao.getProductbyID(prodID)
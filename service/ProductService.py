from dao.ProductDAO import ProductDAO

class ProductService:
    def __init__(self):
        self.product_dao = ProductDAO()

    def get_all_products(self):
        return self.product_dao.get_all_products()

    def get_product_details(self, prodID):
        return self.product_dao.get_product_by_id(prodID)

    def add_product(self, product):
        self.product_dao.add_product(product)

    def update_product(self, product):
        self.product_dao.update_product(product)

    def delete_product(self, prodID):
        self.product_dao.delete_product(prodID)

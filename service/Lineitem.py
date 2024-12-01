from model.Product import Product

class lineItem:
    
    def __init__(self, product: Product, itemQuantity):
        self.itemQuantity = itemQuantity
        self.product = product
        self.totalPrice = product.prodPrice * itemQuantity
    
    def to_dict(self):
        return {
            "product": self.product.to_dict(),  # Serialize the product
            "itemQuantity": self.itemQuantity,
            "totalPrice": convertNumberToPrice(self.totalPrice),  # Format total price as a string
        }
    
    
def convertNumberToPrice(price):
    decimal_places = 2
    formatted_number = f"{price:.{decimal_places}f}"
    return formatted_number
# importing abstract to make the class a parent

class Product:
    # Attributes specific to all products
    def __init__(self, prodID, prodName, prodDesc, prodPrice, 
                 prodStock, prodUsage, uniqeAttribute, prodImage=None):
        
        self.prodID = prodID
        self.prodName = prodName
        self.prodDesc = prodDesc
        self.prodPrice = prodPrice
        self.prodStock = prodStock
        self.prodUsage = prodUsage
        self.uniqeAttribute = uniqeAttribute
        self.prodImage = prodImage

    #Converting product to a dictionary in order to use the shopping cart
    def to_dict(self):
        return {
            "prodID": self.prodID,
            "prodName": self.prodName,
            "prodDesc": self.prodDesc,
            "prodPrice": self.prodPrice,
            "prodStock": self.prodStock,
            "prodUsage": self.prodUsage,
            "uniqeAttribute": self.uniqeAttribute,
            "prodImage": self.prodImage
        }
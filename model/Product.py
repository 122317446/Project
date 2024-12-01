# importing abstract to make the class a parent
'''from abc import ABC, abstractmethod'''

class Product:
    # Attributes specific to all products
    def __init__(self, prodID, prodName, prodDesc, prodPrice, 
                 prodStock, uniqeAttribute, prodImage=None):
        
        self.prodID = prodID
        self.prodName = prodName
        self.prodDesc = prodDesc
        self.prodPrice = prodPrice
        self.prodStock = prodStock
        self.uniqeAttribute = uniqeAttribute
        self.prodImage = prodImage

    def to_dict(self):
        return {
            "prodID": self.prodID,
            "prodName": self.prodName,
            "prodDesc": self.prodDesc,
            "prodPrice": self.prodPrice,
            "prodStock": self.prodStock,
            "uniqeAttribute": self.uniqeAttribute,
            "prodImage": self.prodImage
        }
        
# abstract method will be passed, 
# child classes will have their own implementation of the method (Polymorphism)
#    @abstractmethod
#    def getPrice(self):
#        pass
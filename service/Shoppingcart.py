from service.Lineitem import*

class ShoppingCart: 
    lineItems = [] 

    def __init__(self):
        self.lineItems = [] #Empty list initialised

    def add_item(self, item: lineItem):
        self.lineItems.append(item) #To add items to lineitems into cart
        
    def delete_item(self, product_id):
        # We will find the item by product ID and then remove it.
        for item in self.lineItems:
            if item.product.prodID == product_id:
                self.lineItems.remove(item)
                return True  # Item found and removed
        return False  # Item not found
    

    def update_item(self, product_id, new_quantity):
        # Iterate through line items to find the product to update
        for item in self.lineItems:
            if item.product.prodID == product_id:
                item.itemQuantity = new_quantity  # Set the quantity to the new specified value
                return True  # Item found and updated
        return False  # Item not found
                
    def cartTotal(self):
        cartPrice = 0.0
        for lineItem in self.lineItems: #Loop is created to cycle through the total costs of each product

            cartPrice += lineItem.totalPrice

        return convertNumberToPrice(cartPrice) #Using the function to get a final cost
    
    def to_dict(self): #Using dictionary conversion to fit both python and html format
        return {
            "lineItems": [item.to_dict() for item in self.lineItems],  # Serialize all line items
            "cartTotal": self.cartTotal(),  # Total price formatted as a string
        }
    
    @staticmethod
    def from_dict(data):
        #Reconstruct a ShoppingCart instance from a dictionary.
        cart = ShoppingCart()
        cart.lineItems = [
            lineItem(
                product=Product(**item['product']),  # Reconstruct Product object
                itemQuantity=item['itemQuantity']
            ) for item in data.get('lineItems', [])
        ]
        return cart #Cart format returned
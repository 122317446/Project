#Importing the needed libraries
from urllib import request

from flask import Flask, render_template, request, redirect, url_for, session, flash
from service.ProductService import ProductService
from service.UserService import UserService
from service.Shoppingcart import*

import os, random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) #Secret key is needed in order to enable dynamic user interactions
product_service = ProductService() 
user_service = UserService()
#Calling the needed service classes

@app.route('/') #The index named as productSpread
def show_products():
    products = product_service.get_all_products()
    return render_template('productSpread.html', products=products)

@app.route('/Product/<int:prodID>') #Webpage for individual product
def select_product(prodID): #By using the product ID, it enables the app to gather the needed specific information
    product = product_service.get_product_details(prodID)
    products = product_service.get_all_products()
    random_products = random.sample(products, k=4) #This will randomise the other products to offer below the viewed product
    return render_template('Product.html', product=product, products=random_products)

@app.route('/login', methods=('GET', 'POST')) #GET and POST will be called in order to enable FORM interactions
def loginAccount():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    
        if not email:
            flash("Enter your email!") #Flashing to notify user
        elif not password:
            flash("Enter your password!")
        else:
            if user_service.login(email, password) == True:
                session['user_email'] = email
                return redirect(url_for('adminDash')) #If user is Admin -> redirect to the admin dashboard
            elif user_service.login(email, password) == False:
                session['user_email'] = email #If user is Customer -> redirect back to the product spread
                return redirect(url_for('show_products'))
            else:
                flash("Invalid Email and password!")

    return render_template('login.html')

@app.route('/logout')
def logout(): #Function to pop (reset) the needed sessions back to guest, None is stated in order to pass through empty variables
    session.pop('user_email', None)
    session.pop('shopping_cart', None) 
    session.pop('cart_count', None)
    return redirect(url_for('show_products'))

@app.route('/signup', methods=('GET', 'POST')) #GET and POST will be called in order to enable FORM interactions
def signUp():
    users = user_service.get_all_users()
    '''print(len(users))''' #Debug code in order to count how many users have signed up
    
    if request.method == 'POST':
        firstname = request.form['fname']
        lastname = request.form['lname']
        email = request.form ['email']
        password = request.form['password']
        address = request.form['address']
        phone = request.form['phone']
        
        if user_service.signUp(firstname, lastname, email, password,
                               address, phone) == True:
            '''print(email)
            print(password)''' #Debug code to help remember signing in again (double check)
            flash("Account created!!")
            return redirect(url_for('show_products'))
        elif user_service.userValidation.checkEmail(users, email) == False:
            flash("Email doesn't have the key characters '@' and '.'.")
        elif user_service.userValidation.checkEmail(users, email) == '0':
            flash("Email has already been used!!")
        elif user_service.userValidation.checkPassword(password) == False:
            flash("Password must be at least 10 characters long and have at least one special character")
        else:
            flash("Enter all information!!")
        #Booleans and simple outputs are used in order to simplify logic routing
            
    return render_template('signup.html')

@app.route('/adminpage') #Webpage for admin dashbaord
def adminDash():
    return render_template('adminPage.html')

@app.route('/cart')
def cart():
    if 'user_email' not in session: #If program does not find a user is currently logged in through email session -> login first
        return redirect(url_for('loginAccount'))
    else:
        #Ensure there's a cart in the session
        shopping_cart = session.get('shopping_cart', None)

        #If the cart exists, reconstruct it from the session
        if shopping_cart:
            shopping_cart = ShoppingCart.from_dict(shopping_cart)
            line_items = shopping_cart.lineItems  #List of line items
            cart_total = shopping_cart.cartTotal()  #Total cart price
            item_count = sum(item.itemQuantity for item in line_items)  # otal quantity of items
        else:
            #Empty cart
            line_items = []
            cart_total = 0.0
            item_count = 0

        return render_template('shoppingcart.html', line_items=line_items, cart_total=cart_total, item_count=item_count)
        #Returning the needed variables to update cart basket


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_email' not in session:
        return redirect(url_for('loginAccount'))
    else:
        #Ensure the cart exists in the session
        if 'shopping_cart' not in session:
            session['shopping_cart'] = ShoppingCart().to_dict()

        #Deserialize the cart
        shopping_cart = ShoppingCart.from_dict(session['shopping_cart'])

        #Get data from form
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])

        #Fetch product details
        product = product_service.get_product_details(product_id)

        #Add item to cart
        item = lineItem(product, quantity)
        shopping_cart.add_item(item)

        #Serialize cart and save to session
        session['shopping_cart'] = shopping_cart.to_dict()

        #Update the cart count in the session
        session['cart_count'] = sum(item['itemQuantity'] for item in session['shopping_cart']['lineItems'])

        #Flash message and redirect
        flash(f"{product.prodName} (x{quantity}) added to cart!")
        return redirect(url_for('show_products'))

@app.context_processor
def inject_cart_count(): #This function initialises the webpage cart and creates a 0 item basket to begin with
    cart_count = session.get('cart_count', 0)  # Default to 0 if no items in the cart
    return dict(cart_count=cart_count)

@app.route('/remove_from_cart/<int:product_id>', methods=['GET'])
def remove_from_cart(product_id):
    #Ensure there's a cart in the session
    if 'shopping_cart' in session:
        shopping_cart = ShoppingCart.from_dict(session['shopping_cart'])
        #Remove the item
        shopping_cart.lineItems = [item for item in shopping_cart.lineItems if item.product.prodID != product_id]
        #Save the updated cart to the session
        session['shopping_cart'] = shopping_cart.to_dict() #Translation method
        session['cart_count'] = sum(item.itemQuantity for item in shopping_cart.lineItems)
        flash("Item removed from the cart.", "info")

    return redirect(url_for('cart'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = int(request.form['product_id'])
    action = request.form.get('action')

    shopping_cart = ShoppingCart.from_dict(session.get('shopping_cart', {}))

    if action == 'update':
        new_quantity = int(request.form['quantity'])  #Get the new quantity from form data
        if shopping_cart.update_item(product_id, new_quantity):
            session['shopping_cart'] = shopping_cart.to_dict()  #Save updated cart back to session
            session['cart_count'] = sum(item.itemQuantity for item in shopping_cart.lineItems)
            return redirect(url_for('cart'))
    elif action == 'remove':
        shopping_cart.delete_item(product_id)

    session['shopping_cart'] = shopping_cart.to_dict()
    session['cart_count'] = sum(item.itemQuantity for item in shopping_cart.lineItems)
    
    return redirect(url_for('cart'))



if __name__ == "__main__":
    app.run(debug=True)
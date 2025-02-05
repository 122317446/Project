#Importing the needed libraries
import requests
from urllib import request

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from service.ProductService import ProductService
from service.UserService import UserService
from service.Shoppingcart import*
from API_routes import api_routes

import os, random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) #Secret key is needed in order to enable dynamic user interactions
app.register_blueprint(api_routes)
product_service = ProductService() 
user_service = UserService()
#Calling the needed service classes

# ----- Homepage / base routing ----- #
@app.route('/') #The index / homepage
def show_products():
    products = product_service.get_all_products()
    return render_template('index.html', products=products)

@app.route('/api/stoic-quote', methods=['GET'])
def get_stoic_quote():
    try:
        api_url = "https://stoic.tekloon.net/stoic-quote"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()  # Directly parse JSON
            print("DEBUG: API Response:", data)  # Debugging step
            
            # Return the response exactly as received
            return jsonify(data), 200
        else:
            print(f"DEBUG: API Error - Status Code {response.status_code}")
            return jsonify({"error": "Failed to fetch quote"}), response.status_code
    except Exception as e:
        print("DEBUG: Exception occurred:", str(e))
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route('/search', methods=['GET'])
def search():
    products = product_service.get_all_products()
    query = request.args.get('q', '').lower()
    if query:
        suggestions = [product for product in products if query in product.prodName.lower()]
    else:
        suggestions = []
    return jsonify([product.to_dict() for product in suggestions]) #Used Flask to_dict() in order to return values correctly

@app.route('/product/<int:prodID>') #Webpage for individual product
def select_product(prodID): #By using the product ID, it enables the app to gather the needed specific information
    product = product_service.get_product_details(prodID)
    products = product_service.get_all_products()
    random_products = random.sample(products, k=4) #This will randomise the other products to offer below the viewed product
    return render_template('product.html', product=product, products=random_products)

# ----- User Login, Logout, Signup routing  ----- #
@app.route('/login', methods=('GET', 'POST')) #GET and POST will be called in order to enable FORM interactions
def loginAccount():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = user_service.login(email, password)
        
        if user:
            session['user_firstName'] = user.firstName

            if user.isAdmin:
                return redirect(url_for('adminDash'))
            else:
                return redirect(url_for('show_products')) #If user is Admin -> redirect to the admin dashboard
        else:
            flash("Invalid Email and password!")

    return render_template('login.html')

@app.route('/logout')
def logout(): #Function to pop (reset) the needed sessions back to guest, None is stated in order to pass through empty variables
    session.pop('user_firstName', None)
    session.pop('shopping_cart', None) 
    session.pop('cart_count', None)
    flash('Successfuly signed out!')
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

# ----- Cart routing ----- #
@app.route('/cart')
def cart():
    if 'user_firstName' not in session: #If program does not find a user is currently logged in through email session -> login first
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
    if 'user_firstName' not in session:
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


# ----- Admin page routing  ----- #
@app.route('/adminpage') #Webpage for admin dashbaord
def adminDash():
    return render_template('adminPage.html')

# PRODUCT & USER CRUD
#--------------
# CREATE
@app.route('/create_product', methods=['POST'])
def create_product():
    try:
        print("Create Product Request Received")
        print("Form Data:", request.form)

        # Convert form data into a Product object
        new_product = Product(
            None,  # Auto-incremented in DB
            request.form.get('prodName', ''),
            request.form.get('prodDesc', ''),
            float(request.form.get('prodPrice', 0)),
            int(request.form.get('prodStock', 0)),
            request.form.get('prodUsage', ''),
            request.form.get('uniqeAttribute', '').split(','),  # Convert CSV string to list
            request.files['prodImage'].filename if 'prodImage' in request.files else None
        )

        # Pass the Product object to ProductService
        new_product_id = product_service.add_product(new_product)

        return jsonify({"message": "Product created successfully!", "prodID": new_product_id}), 201

    except Exception as e:
        print("Error creating product:", str(e))  # Log error
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500

# RETREIVE
@app.route('/manageProd')
def manageProd():
    products = product_service.get_all_products()
    return render_template('adminProd.html', products=products)
@app.route('/manageUser')
def manageUser():
    users = user_service.get_all_users()
    return render_template('adminUser.html', users=users)

# UPDATE
@app.route('/updateProd/<int:prodID>', methods=['POST'])
def updateProd(prodID):
    try:
        print(f"Update Request Received for Product ID: {prodID}")

        # Retrieve the product from the database
        product = product_service.get_product_details(prodID)
        if not product:
            return jsonify({"message": "Product not found!"}), 404

        # Update product details
        product.prodName = request.form.get('prodName', '')
        product.prodDesc = request.form.get('prodDesc', '')
        product.prodPrice = float(request.form.get('prodPrice', 0))
        product.prodStock = int(request.form.get('prodStock', 0))
        product.prodUsage = request.form.get('prodUsage', '')
        product.uniqeAttribute = request.form.get('uniqeAttribute', '').split(',')

        # Handle image update (if a new image is uploaded)
        if 'prodImage' in request.files:
            prodImage = request.files['prodImage']
            if prodImage.filename:
                image_filename = prodImage.filename
                prodImage.save(f"static/images/{image_filename}")
                product.prodImage = image_filename  # Update product image if changed

        # Now pass the Product object to ProductService
        product_service.update_product(product)

        return jsonify({"message": "Product updated successfully!"}), 200

    except Exception as e:
        print("Error updating product:", str(e))
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500
@app.route('/updateUser/<int:userID>', methods=['POST'])
def updateUser(userID):
    try:
        print(f"Update Request Received for User ID: {userID}")

        # Retrieve user from DB
        user = user_service.get_user_details(userID)
        if not user:
            return jsonify({"message": "User not found!"}), 404

        # Update user details
        user.firstName = request.form.get('firstName', '')
        user.lastName = request.form.get('lastName', '')
        user.userEmail = request.form.get('userEmail', '')
        user.userAdress = request.form.get('userAdress', '')
        user.userPhone = request.form.get('userPhone', '')

        # Call service to update user
        user_service.update_user(user)

        return jsonify({"message": "User updated successfully!"}), 200

    except Exception as e:
        print("Error updating user:", str(e))
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500

# DELETE
@app.route('/deleteProd/<int:prodID>', methods=['DELETE'])
def deleteProd(prodID):
    try:
        print(f"Delete Request Received for Product ID: {prodID}")

        # Check if product exists before deletion
        product = product_service.get_product_details(prodID)
        if not product:
            return jsonify({"message": "Product not found!"}), 404

        # Delete the product
        product_service.delete_product(prodID)

        return jsonify({"message": "Product deleted successfully!"}), 200

    except Exception as e:
        print("Error deleting product:", str(e))
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500
@app.route('/deleteUser/<int:userID>', methods=['DELETE'])
def deleteUser(userID):
    try:
        print(f"Delete Request Received for User ID: {userID}")

        # Check if user exists before deletion
        user = user_service.get_user_details(userID)
        if not user:
            return jsonify({"message": "User not found!"}), 404

        # Delete user
        user_service.delete_user(userID)

        return jsonify({"message": "User deleted successfully!"}), 200

    except Exception as e:
        print("Error deleting user:", str(e))
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
from urllib import request

from flask import Flask, render_template, request, redirect, url_for, session, flash
from service.ProductService import ProductService
from service.UserService import UserService
from service.Shoppingcart import*

import os, random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
product_service = ProductService()
user_service = UserService()

@app.route('/')
def show_products():
    products = product_service.get_all_products()
    return render_template('ProductSpread.html', products=products)

@app.route('/Product/<int:prodID>')
def select_product(prodID):
    product = product_service.get_product_details(prodID)
    products = product_service.get_all_products()
    random_products = random.sample(products, k=4)
    return render_template('Product.html', product=product, products=random_products)

@app.route('/login', methods=('GET', 'POST'))
def loginAccount():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    
        if not email:
            flash("Enter your email!")
        elif not password:
            flash("Enter your password!")
        else:
            if user_service.login(email, password) == True:
                session['user_email'] = email
                return redirect(url_for('adminDash'))
            elif user_service.login(email, password) == False:
                session['user_email'] = email
                return redirect(url_for('show_products'))
            else:
                print("else")
                return redirect(url_for('loginAccount'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_email')
    session.pop('shopping_cart') 
    session.pop('cart_count')
    return redirect(url_for('show_products'))

@app.route('/signup', methods=('GET', 'POST'))
def signUp():
    users = user_service.get_all_users()
    print(len(users))
    
    if request.method == 'POST':
        firstname = request.form['fname']
        lastname = request.form['lname']
        email = request.form ['email']
        password = request.form['password']
        address = request.form['address']
        phone = request.form['phone']
        
        if user_service.signUp(firstname, lastname, email, password,
                               address, phone) == True:
            print(email)
            print(password)
            return redirect(url_for('show_products'))
        else:
            print("False")
            
    return render_template('signup.html')

@app.route('/adminpage')
def adminDash():
    return render_template('adminPage.html')

@app.route('/cart')
def cart():
    if 'user_email' not in session:
        return redirect(url_for('loginAccount'))
    else:
        # Ensure there's a cart in the session
        shopping_cart = session.get('shopping_cart', None)

        # If the cart exists, reconstruct it from the session
        if shopping_cart:
            shopping_cart = ShoppingCart.from_dict(shopping_cart)
            line_items = shopping_cart.lineItems  # List of line items
            cart_total = shopping_cart.cartTotal()  # Total cart price
            item_count = sum(item.itemQuantity for item in line_items)  # Total quantity of items
        else:
            # Empty cart
            line_items = []
            cart_total = 0.0
            item_count = 0

        return render_template('shoppingcart.html', line_items=line_items, cart_total=cart_total, item_count=item_count)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_email' not in session:
        return redirect(url_for('loginAccount'))
    else:
        # Ensure the cart exists in the session
        if 'shopping_cart' not in session:
            session['shopping_cart'] = ShoppingCart().to_dict()

        # Deserialize the cart
        shopping_cart = ShoppingCart.from_dict(session['shopping_cart'])

        # Get data from form
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])

        # Fetch product details
        product = product_service.get_product_details(product_id)

        # Add item to cart
        item = lineItem(product, quantity)
        shopping_cart.add_item(item)

        # Serialize cart and save to session
        session['shopping_cart'] = shopping_cart.to_dict()

        # Update the cart count in the session
        session['cart_count'] = sum(item['itemQuantity'] for item in session['shopping_cart']['lineItems'])

        # Flash message and redirect
        flash(f"{product.prodName} (x{quantity}) added to cart!", "success")
        return redirect(url_for('show_products'))

@app.context_processor
def inject_cart_count():
    cart_count = session.get('cart_count', 0)  # Default to 0 if no items in the cart
    return dict(cart_count=cart_count)

@app.route('/remove_from_cart/<int:product_id>', methods=['GET'])
def remove_from_cart(product_id):
    # Ensure there's a cart in the session
    if 'shopping_cart' in session:
        shopping_cart = ShoppingCart.from_dict(session['shopping_cart'])
        # Remove the item
        shopping_cart.lineItems = [item for item in shopping_cart.lineItems if item.product.prodID != product_id]
        # Save the updated cart to the session
        session['shopping_cart'] = shopping_cart.to_dict()
        session['cart_count'] = sum(item.itemQuantity for item in shopping_cart.lineItems)
        flash("Item removed from the cart.", "info")

    return redirect(url_for('cart'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = int(request.form['product_id'])
    action = request.form.get('action')

    shopping_cart = ShoppingCart.from_dict(session.get('shopping_cart', {}))

    if action == 'update':
        new_quantity = int(request.form['quantity'])  # Get the new quantity from form data
        if shopping_cart.update_item(product_id, new_quantity):
            session['shopping_cart'] = shopping_cart.to_dict()  # Save updated cart back to session
            session['cart_count'] = sum(item.itemQuantity for item in shopping_cart.lineItems)
            return redirect(url_for('cart'))
    elif action == 'remove':
        shopping_cart.delete_item(product_id)

    session['shopping_cart'] = shopping_cart.to_dict()
    session['cart_count'] = sum(item.itemQuantity for item in shopping_cart.lineItems)
    
    return redirect(url_for('cart'))



if __name__ == "__main__":
    app.run(debug=True)
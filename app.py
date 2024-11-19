from urllib import request

from flask import Flask, render_template, request, redirect, url_for, session, flash
from service.ProductService import ProductService
from service.UserService import UserService
import os

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
    return render_template('Product.html', product=product, products=products)

@app.route('/login', methods=('GET', 'POST'))
def loginAccount():
    if request.method == 'POST':
        Email = request.form['email']
        Password = request.form['password']
    
        if not Email:
            flash("Enter your email!")
        elif not Password:
            flash("Enter your password!")
        else:
            if user_service.login(Email, Password) == True:
                return redirect(url_for('show_products'))
            elif user_service.login(Email, Password) == None:
                return redirect(url_for('signUp'))
            else:
                flash("USER IS NOT FOUND!")

    return render_template('login.html')

@app.route('/signup')
def signUp():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)
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
        email = request.form['email']
        password = request.form['password']
    
        if not email:
            flash("Enter your email!")
        elif not password:
            flash("Enter your password!")
        else:
            if user_service.login(email, password) == True:
                return redirect(url_for('show_products'))
            elif user_service.login(email, password) == False:
                return redirect(url_for('signUp'))
            else:
                print("else")
                return redirect(url_for('loginAccount'))

    return render_template('login.html')

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

if __name__ == "__main__":
    app.run(debug=True)
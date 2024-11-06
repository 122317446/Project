from urllib import request

from flask import Flask, render_template, request, redirect, url_for, session, flash
from service.ProductService import ProductService
'''from service.UserService import UserService'''

app = Flask(__name__)
product_service = ProductService()

@app.route('/')
def Landing_Page():
    return render_template('LandingPage.html')

@app.route('/Productlistings')
def show_products():
    products = product_service.get_all_products()
    return render_template('Productlistings.html', products=products)

if __name__ == "__main__":
    app.run(debug=True)
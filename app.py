from urllib import request

from flask import Flask, render_template, request, redirect, url_for, session, flash
from service.ProductService import ProductService
'''from service.UserService import UserService'''

app = Flask(__name__)
product_service = ProductService()

@app.route('/')
def show_products():
    products = product_service.get_all_products()
    return render_template('ProductSpread.html', products=products)

'''@app.route('/page2')
def Landing_Page():
    return render_template('LandingPage.html')'''

if __name__ == "__main__":
    app.run(debug=True)
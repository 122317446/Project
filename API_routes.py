from flask import Blueprint, request, jsonify
from dao.ProductDAO import ProductDAO

# Create a blueprint for the API routes
api_routes = Blueprint('api_routes', __name__)

# Define the filter_products route
@api_routes.route('/api/filter_products', methods=['GET'])
def filter_products():
    # Get filter parameters from the request
    usage = request.args.get('usage', '')  # Defaults to empty string
    price_min = float(request.args.get('price_min', 0))  # Defaults to 0
    price_max = float(request.args.get('price_max', 1e9))  # Defaults to a very high number
    sort_order = request.args.get('sort', 'asc')  # Defaults to ascending order

    # Query the database for filtered products
    dao = ProductDAO()
    products = dao.filter_products(usage, price_min, price_max, sort_order)

    # Convert product objects to dictionaries and return as JSON
    return jsonify([product.to_dict() for product in products])
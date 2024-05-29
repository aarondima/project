from flask import Blueprint, jsonify, request
from db import db
from models import Order, Customer, Product, ProductOrder
# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
api_products_bp = Blueprint("api_products", __name__)

@api_products_bp.route("/", methods=["POST"])
def api_create_product():
    data = request.json
    if "name" not in data or "price" not in data:
        return "Invalid request", 400
    if (data['price'] <= 0):
        return "Invalid price", 400
    if not isinstance(data['available'], (int)) or data['available'] < 0:
        return "Invalid available", 400
    product = Product(name=data['name'], price=data['price'], available=data['available'])
    db.session.add(product)
    db.session.commit()
    return "Success", 201

@api_products_bp.route("/<int:product_id>", methods=["PUT"])
def api_update_product(product_id):
    data = request.json
    product = Product.query.get_or_404(product_id)
    if "name" not in data or "price" not in data or "available" not in data:
        return "Invalid request", 400
    price = data['price']
    name = data['name']
    available = data['available']
    if not isinstance(price, (int,float)) or price < 0:
        return "Invalid price", 400
    if not isinstance(available, (int)) or available < 0:
        return "Invalid available", 400
    
    product.name = name
    product.price = price
    product.available = available
    db.session.commit()
    return "Success", 204
@api_products_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return "deleted", 204

@api_products_bp.route("/final/warning", methods=["POST"])
def find_below_threshold():
    data = request.json
    if "threshold" not in data:
        return "Invalid request", 400
    threshold = data["threshold"]
    if not isinstance(threshold, int):
        return "Invalid threshold", 418
    stmt = db.select(Product).order_by(Product.name)
    results = db.session.execute(stmt).scalars()
    products = []
    for product in results:
        if (product.available < threshold):
            json_record = {
                "name": product.name,
                "available": product.available
            }
            products.append(json_record)
    json_list = {
        "products": products,
        "threshold": threshold,
    }
    return jsonify(json_list)
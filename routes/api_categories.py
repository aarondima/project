from flask import Blueprint, jsonify, request
from db import db
from models import Order, Customer, Product, ProductOrder, Category

api_categories_bp = Blueprint("api_categories", __name__)

@api_categories_bp.route("/", methods=["POST"])
def get_categories():
    stmt = db.select(Category).order_by(Category.name)
    results = db.session.execute(stmt).scalars()
    categories = []
    for category in results:
        products = []
        for product in category.product:
            json_product ={
                "name": product.name,
                "url": (f"/product/{product.id}")
            }
            products.append(json_product)
        json_record = {
            "name": category.name,
            "description": category.description,
            "products": products
        }
        categories.append(json_record)
    return jsonify(categories)
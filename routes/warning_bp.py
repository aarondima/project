from flask import Blueprint, render_template, redirect, url_for, jsonify
from db import db
from models import Order, Customer, Product
# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
warning_bp = Blueprint("warning", __name__)

@warning_bp.route("/customers-warning")
def customer_warning():
    stmt = db.select(Customer).order_by(Customer.name)
    results = db.session.execute(stmt).scalars()
    customers = []
    for customer in results:
        if(customer.balance <= 0):
            json_record = {
                "name": customer.name,
                "balance": customer.balance,
                "url": (f"/api/customers/{customer.id}")
            }
            customers.append(json_record)
    return jsonify(customers)

@warning_bp.route("/out-of-stock")
def out_of_stock():
    stmt = db.select(Product).order_by(Product.name)
    results = db.session.execute(stmt).scalars()
    products = []
    for product in results:
        if(product.available == 0):
            json_record = {
                "name": product.name
            }
            products.append(json_record)
    return jsonify(products)
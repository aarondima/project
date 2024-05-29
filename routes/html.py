from flask import Blueprint, render_template, redirect, url_for
from db import db
from models import Order, Customer, Product
# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
html_bp = Blueprint("html", __name__)

@html_bp.route("/")
def homepage():
    return render_template("home.html", name="Aaron")

@html_bp.route("/customer")
def customers():
    statement = db.select(Customer).order_by(Customer.name)
    records = db.session.execute(statement)
    customers = records.scalars().all()
    return render_template("customers.html", customers=customers)
@html_bp.route("/customer/<int:customer_id>")
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer:
        return render_template("customerInfo.html",customerOrders=customer.orders)
    else:
        return "Customer not found", 404    
@html_bp.route("/products")
def products():
    statement = db.select(Product).order_by(Product.name)
    records = db.session.execute(statement)
    products = records.scalars().all()
    return render_template("products.html", products=products)

@html_bp.route("/orders")
def orders():
    statement = db.select(Order).order_by(Order.id)
    records = db.session.execute(statement)
    orders = records.scalars().all()
    return render_template("orders.html", orders=orders)

@html_bp.route("/orders/<int:order_id>")
def get_order(order_id):
    orders = Order.query.get_or_404(order_id)
    total = orders.get_total()
    return render_template("orderInfo.html",orders=orders, total=total)

@html_bp.route("/orders/<int:order_id>/process", methods=["POST"])
def process_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.process()
    return redirect(url_for("html.orders"))
@html_bp.route("/<int:order_id>/delete", methods=["POST"])
def order_delete(order_id):
    order = Order.query.get_or_404(order_id)
    if order.processed:
        return "Order has been already processed", 418
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("html.orders"))
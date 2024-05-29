from flask import Blueprint, jsonify, request
from db import db
from models import Order, Customer, Product, ProductOrder
# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
api_orders_bp = Blueprint("api_orders", __name__)

@api_orders_bp.route("/", methods=['POST'])
def api_create_order():
    data = request.json
    customer_id = data["customer_id"]
    customer = Customer.query.get_or_404(customer_id)
    order = Order(customer=customer)
    db.session.add(order)
    for orderItem in data["items"]:

        product = db.session.query(Product).filter_by(name=orderItem["name"]).first()
        if(product == None):
            return "Invalid product", 400
        quantity = orderItem["quantity"]
        if not isinstance(quantity,(int)):
            return "Invalid quantity", 400
        if (quantity <= 0):
            return "Invalid quantity", 400
        item = ProductOrder(order=order,product=product,quantity=quantity)
        db.session.add(item)
    db.session.commit()
    return "Order Created",200

@api_orders_bp.route("/<int:order_id>", methods=["PUT"])
def process_order_api(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.json
    strategy="adjust"
    if "process" not in data or data['process'] != True:
        return "Invalid request", 400
    if "strategy" in data:
        strategy = data['strategy']
    order.process(strategy)
    return "Order processed", 200
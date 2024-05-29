from flask import Blueprint, jsonify, request, current_app
from db import db
from models import Customer
# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
api_customers_bp = Blueprint("api_customers", __name__)

@api_customers_bp.route("/", methods=["GET"])
def api_customer_list():
    stmt = db.select(Customer).order_by(Customer.name)
    results = db.session.execute(stmt).scalars()
    return jsonify([cust.to_json() for cust in results])

@api_customers_bp.route("/<int:customer_id>", methods=["GET"])
def api_customer_info(customer_id):
    statement = db.select(Customer).where(Customer.id == customer_id)
    result = db.session.execute(statement)
    customer = result.scalar_one()
    json_record = { "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "balance": customer.balance,}
    return jsonify(json_record)
@api_customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def api_customer_delete(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return "deleted", 204
@api_customers_bp.route("/", methods=["POST"])
def api_create_customer():
    data = request.json
    if "name" not in data or "phone" not in data:
        return "Invalid request", 400
    
    customer = Customer(name=data['name'], phone=data['phone'])
    db.session.add(customer)
    db.session.commit()
    return "Success", 201
@api_customers_bp.route("/<int:customer_id>", methods=["PUT"])
def api_update_balance(customer_id):
    data = request.json
    customer = db.get_or_404(Customer, customer_id)

    if "balance" not in data:
        return "Invalid request: balance missing", 400

    balance = data["balance"]

    if not isinstance(balance, (int, float)):
        return "Invalid request: balance must be a number", 400

    customer.balance = balance
    db.session.commit()

    return "Successfully updated", 204
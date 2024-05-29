from flask import Flask, jsonify, render_template, request, redirect, url_for
from db import db
from pathlib import Path
from models import Customer, Product, Order, ProductOrder
from routes.api_customers import api_customers_bp
from routes.api_orders import api_orders_bp
from routes.api_products import api_products_bp
from routes.html import html_bp
from routes.warning_bp import warning_bp
from routes.api_categories import api_categories_bp
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///i_copy_pasted_this.db"
# This will make Flask store the database file in the path provided
app.instance_path = Path("change_this").resolve()
# Adjust to your needs / liking. Most likely, you want to use "." for your instance
# path. You may also use "data".

db.init_app(app)

app.register_blueprint(api_customers_bp, url_prefix="/api/customers")
app.register_blueprint(api_orders_bp, url_prefix="/api/orders")
app.register_blueprint(api_products_bp, url_prefix="/api/products")
app.register_blueprint(html_bp, url_prefix="/")
app.register_blueprint(warning_bp, url_prefix="/final")
app.register_blueprint(api_categories_bp, url_prefix="/api/categories")
# app.register_blueprint(api_customers_bp, url_prefix="/api/customers/")
# @app.route("/")
# def home():
#     return render_template("home.html", name="Aaron")

# @app.route("/customers")
# def customers():
#     statement = db.select(Customer).order_by(Customer.name)
#     records = db.session.execute(statement)
#     customers = records.scalars().all()
#     return render_template("customers.html", customers=customers)

# @app.route("/customers/<int:customer_id>")
# def get_customer(customer_id):
#     customer = Customer.query.get_or_404(customer_id)
#     if customer:
#         return render_template("customerInfo.html",customerOrders=customer.orders)
#     else:
#         return "Customer not found", 404    

# @app.route("/products")
# def products():
#     statement = db.select(Product).order_by(Product.name)
#     records = db.session.execute(statement)
#     products = records.scalars().all()
#     return render_template("products.html", products=products)

# @app.route("/orders")
# def orders():
#     statement = db.select(Order).order_by(Order.id)
#     records = db.session.execute(statement)
#     orders = records.scalars().all()
#     return render_template("orders.html", orders=orders)
# @app.route("/orders/<int:order_id>")
# def get_order(order_id):
#     orders = Order.query.get_or_404(order_id)
#     total = orders.get_total()
#     return render_template("orderInfo.html",orders=orders, total=total)
# @app.route("/orders/<int:order_id>/process", methods=["POST"])
# def process_order(order_id):
#     order = Order.query.get_or_404(order_id)
#     order.process()
#     return redirect(url_for("orders"))
# @app.route("/api/orders", methods=['POST'])
# def create_order():
#     data = request.json
#     customer_id = data["customer_id"]
#     customer = Customer.query.get_or_404(customer_id)
#     order = Order(customer=customer)
#     db.session.add(order)
#     for orderItem in data["items"]:
#         product = db.session.query(Product).filter_by(name=orderItem["name"]).first()
#         quantity = orderItem["quantity"]
#         item = ProductOrder(order=order,product=product,quantity=quantity)
#         db.session.add(item)
#     db.session.commit()
#     return "Order Created",200
            
# @app.route("/api/customer")
# def customers_json():
#     statement = db.select(Customer).order_by(Customer.name)
#     results = db.session.execute(statement)
#     customers = [] # output variable
#     for customer in results.scalars().all():
#         json_record = {
#             "id": customer.id,
#             "name": customer.name,
#             "phone": customer.phone,
#             "balance": customer.balance,
#         }
#     customers.append(json_record)
#     return jsonify(customers)
# @app.route("/api/customers/<int:customer_id>")
# def customer_detail_json(customer_id):
#     statement = db.select(Customer).where(Customer.id == customer_id)
#     result = db.session.execute(statement)
#     customer = result.scalar_one()
#     json_record = { "id": customer.id,
#             "name": customer.name,
#             "phone": customer.phone,
#             "balance": customer.balance,}
#     return jsonify(json_record)

# @app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
# def customer_delete(customer_id):
#     customer = db.get_or_404(Customer, customer_id)
#     db.session.delete(customer)
#     db.session.commit()
#     return "deleted", 204

# @app.route("/api/customers", methods=["POST"])
# def create_customer():
#     data = request.json
#     if "name" not in data or "phone" not in data:
#         return "Invalid request", 400
#     with app.app_context():
#         customer = Customer(name=data['name'], phone=data['phone'])
#         db.session.add(customer)
#         db.session.commit()
#     return "Success", 201

# @app.route("/api/customers/<int:customer_id>", methods=["PUT"])
# def update_balance(customer_id):
#     data = request.json
#     customer = db.get_or_404(Customer, customer_id)

#     if "balance" not in data:
#         return "Invalid request", 400
#     balance = data["balance"]

#     if not isinstance(balance, (int, float)):
#         return "Invalid request: balance", 400
#     customer.balance = balance

#     db.session.commit()
#     return "Successfully updated", 204

# @app.route("/api/products", methods=["POST"])
# def create_product():
#     data = request.json
#     if "name" not in data or "price" not in data:
#         return "Invalid request", 400
#     with app.app_context():
#         product = Product(name=data['name'], price=data['price'])
#         db.session.add(product)
#         db.session.commit()
#     return "Success", 201

# @app.route("/api/products/<int:product_id>", methods=["PUT"])
# def update_product(product_id):
#     data = request.json
#     product = Product.query.get_or_404(product_id)
#     if "name" not in data or "price" not in data:
#         return "Invalid request", 400
#     price = data['price']
#     name = data['name']
#     if not isinstance(price, (int,float)):
#         return "Invalid request", 400
#     product.name = name
#     product.price = price
#     db.session.commit()
#     return "Success", 204
# @app.route("/api/products/<int:product_id>", methods=["DELETE"])
# def delete_product(product_id):
#     product = Product.query.get_or_404(product_id)
#     db.session.delete(product)
#     db.session.commit()
#     return "deleted", 204

# @app.route("/orders/<int:order_id>/delete", methods=["POST"])
# def order_delete(order_id):
#     order = Order.query.get_or_404(order_id)
#     if order.processed:
#         return "Order has been already processed", 418
#     db.session.delete(order)
#     db.session.commit()
#     return redirect(url_for("orders"))


# @app.route("/api/orders/<int:order_id>", methods=["PUT"])
# def process_order_api(order_id):
#     order = Order.query.get_or_404(order_id)
#     data = request.json
#     strategy="adjust"
#     if "process" not in data or data['process'] != True:
#         return "Invalid request", 400
#     if "strategy" in data:
#         strategy = data['strategy']
#     order.process(strategy)
#     return "Order processed", 200
if __name__ == "__main__":
    app.run(debug=True, port=8888)
from db import db
from app import app
import csv
from models import Customer, Product, Order, ProductOrder, Category
from sqlalchemy.sql import functions as func
import random

def create_all_tables():
    with app.app_context():
        db.create_all()
def delete_all_tables():
    with app.app_context():
        db.drop_all()
def load_all():
    with app.app_context():
        with open("data/customers.csv", newline= '') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rand_bal = random.randint(-150,20)
                customer = Customer(name=row['name'], phone=row['phone'],balance=rand_bal)
                db.session.add(customer)
        with open("data/productsCat.csv", newline= '') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rand_qty = random.randint(0,1)
                category = Category(name=row['category'])
                db.session.add(category)
                product = Product(name=row['name'], price=row['price'],category=category.name,available=rand_qty )
                db.session.add(product)
        db.session.commit()

def random_db():
    with app.app_context():
        # Find a random customer
        for _ in range(100):
            cust_stmt = db.select(Customer).order_by(func.random()).limit(1)
            customer = db.session.execute(cust_stmt).scalar()
            order = Order(customer=customer)
            db.session.add(order)
            rand_prod_qty = random.randint(1,6)
            for _ in range(rand_prod_qty):

            # Find a random product
                prod_stmt = db.select(Product).order_by(func.random()).limit(1)
                product = db.session.execute(prod_stmt).scalar()
                rand_qty = random.randint(10, 20)
                # Add that product to the order
                association_1 = ProductOrder(order=order, product=product, quantity=rand_qty)
                db.session.add(association_1)
            
        db.session.commit()
if __name__ == "__main__":
    delete_all_tables()
    create_all_tables()
    load_all()
    random_db()
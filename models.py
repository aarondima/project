from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from db import db
from sqlalchemy.sql import func

class Customer(db.Model):
    orders = relationship("Order", cascade="all, delete-orphan")
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    phone = mapped_column(String(20), nullable=False)
    balance = mapped_column(Float(precision=10), nullable=False, default=0.00)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "balance": self.balance
        }
class Product(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    price = mapped_column(Numeric(10,2), nullable=False)
    available = mapped_column(Integer, nullable=False)
    category = relationship("Category", back_populates="product")
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }
    orderProducts = relationship("ProductOrder")
    
class Order(db.Model):
    id = mapped_column(Integer, primary_key=True)
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False)
    customer = relationship("Customer", back_populates="orders")
    total = mapped_column(Integer, nullable=False,default=0)
    items = relationship("ProductOrder", cascade="all, delete-orphan")
    def get_total(self):
        total = 0
        for product in self.items:
            totalProduct = round(float(product.product.price)*product.quantity)
            total += totalProduct
        return total
    created = mapped_column(DateTime, nullable=False, default=func.now())
    processed = mapped_column(DateTime, nullable=True, default=None)
    def process(self, strategy="adjust"):
        if(self.processed != None):
            return True, "Order already processed"
        if(self.customer.balance <= 0):
            return False, "Balance insufficient"
        total_price = 0
        for item in self.items:
            product = Product.query.get_or_404(item.product_id)
            if(item.quantity > product.available):
                match strategy:
                    case "adjust":
                        item.quantity = product.available
                        product.available = 0
                    case "reject":
                        return False, "Order can't be processed"
                    case "ignore":
                        item.quantity = 0
            else:
                product.available -= item.quantity
            total_price = total_price + item.quantity*product.price
        self.customer.balance -= float(total_price)
        self.processed = func.now()
        db.session.commit()
        return True, "Process good"
    
class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey(Order.id), nullable=False)
    order = relationship("Order", back_populates="items")

    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    product = relationship("Product", back_populates="orderProducts")
    quantity = mapped_column(Integer, nullable=False, default=0)

class Category(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    description = mapped_column(String(500), nullable=False, default="N/A")
    product_id = mapped_column(Integer, ForeignKey(Product.id))
    product = relationship("Product", back_populates="category")
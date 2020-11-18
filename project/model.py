from datetime import datetime
from project import db

orderdetails = db.Table('orderdetail',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), nullable=False),
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), nullable=False),
)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    type = db.Column(db.Integer, nullable=False)
    displayCost = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.type}', '{self.cost}', '{self.image_file}')"


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    totalcost = db.Column(db.Integer, nullable=False)
    date_of_order = db.Column(db.DateTime, nullable=False, default=datetime.now())
    displayCost = db.Column(db.String, nullable=False)
    product_id = db.relationship('Product', secondary=orderdetails , backref='product', lazy=True)

    def __repr__(self):
        return f"Order('{self.name}', '{self.date_of_order}', '{self.totalcost}')"



from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pytz
indian_timezone = pytz.timezone('Asia/Kolkata')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus.db'
db = SQLAlchemy(app)

indian_timezone = pytz.timezone('Asia/Kolkata')

class User(db.Model):
    __tablename__ = "User"
    uid = db.Column(db.Integer,autoincrement=True,nullable=False,primary_key = True)
    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    mobileno = db.Column(db.String,nullable=True)
    adrress = db.Column(db.String,nullable=True)
    pin = db.Column(db.Integer,nullable = True)


class Product(db.Model):
    __tablename__ = "Product"
    pID = db.Column(db.Integer,autoincrement = True,nullable=False,primary_key = True)
    name = db.Column(db.String,nullable=False)
    mrp = db.Column(db.Integer,nullable = False)
    sellingPrice = db.Column(db.Integer,nullable = False)
    discount = db.Column(db.Integer,nullable = False)
    stock = db.Column(db.Integer,nullable = False)
    tabDescription = db.Column(db.String,nullable = False)
    imgurl = db.Column(db.String,nullable = False)




class CartItem(db.Model):
    __tablename__ = "Cart Item"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.pID'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.uid'), nullable=False)
    pname = db.Column(db.String,nullable = False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    __tablename__ = "Order"
    orderId = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.uid'), nullable=False)
    orderDate = db.Column(db.DateTime, default=datetime.now(indian_timezone))
    totalAmount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.now(indian_timezone))


class OrderItems(db.Model):
    __tablename__ = 'OrderItems'
    orderItemId = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.pID'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.uid'), nullable=False)
    product_name = db.Column(db.String, nullable= False)
    order_id = db.Column(db.Integer, db.ForeignKey('Order.orderId'), nullable=False)
    quantity = db.Column(db.Integer,nullable = False)
    subtotal = db.Column(db.Integer,nullable = False)
    orderDate = db.Column(db.DateTime, default=indian_timezone)


    
   

    
    

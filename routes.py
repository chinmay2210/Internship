import os
import random
from flask import redirect, render_template, request,session
import razorpay
from datetime import datetime
from database import Order, OrderItems,indian_timezone, app,User,db,Product,CartItem
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app.secret_key = 'sskey'
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html",products = products)



#------------------User Login and Register-------------------------
def generate_verification_token():
    return str(random.randint(100000, 999999))

@app.route("/signUp",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        email = email.lower()
        password = request.form["password"]
        fpass = request.form["fpass"]
        

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            pas = 3
            print("user exits")
            return render_template("login.html",pas = pas)
        
        if(password==fpass):
            otp = generate_verification_token()
            session["otp"] = otp
            session["name"] = name
            session["email"] = email
            session["password"] = password
            
            send_email(email, otp,name)
            return render_template('otp.html')
        else:
             pas = 4
             return render_template("login.html",pas = pas)
    
   
    return render_template("login.html")

@app.route("/emailVerification",methods=["GET","POST"])
def verification():
    if request.method == 'POST':
        submitted_otp = request.form["otp"] 
        email = session.get("email") 
        otp = session.get("otp")

        if email and otp and submitted_otp == otp:
            user = User(name=session.get("name"), email=session.get("email"), password=session.get("password"))
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(email = email).first()
            session['name'] = user.name
            session['uid'] = user.uid
            session['email'] = user.email
            return redirect("/")
        else:
            pas = 5
            return render_template("otp.html",pas = pas)
    return render_template("otp.html")

def send_email(receiver_email, otp,name):
    # Set up the MIMEText object to represent the email body
    sender_email ="codestream63@gmail.com"
    sender_password = "tkdcwqrlnkvxxirj"
   
    subject =  "Company name - Your OTP Inside"
    body = f'''Hello {name}\n{otp}'''
  
    
    
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server with TLS
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # Enable debugging to see communication with the server (optional)
        server.set_debuglevel(1)

        # Log in to the SMTP server with your email credentials
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # Enable debugging to see communication with the server (optional)
        server.set_debuglevel(1)

        # Log in to the SMTP server with your email credentials
        server.login("codestream74@gmail.com", "fyhmgapeexvlqkuf")

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
    finally:
        # Close the connection to the SMTP server
        server.quit()


@app.route("/userDetails",methods=['GET','POST'])
def orderdetl():
    if 'uid' not in session:
        # User is not logged in, redirect to the login page
        return redirect("/login")
    uid = session['uid']
    user = User.query.filter_by(uid = uid).first()
    if request.method == 'POST':
        pin = request.form['pin']
        adrress = request.form['adrress']
        phoneno = request.form['phoneno']

        user = User.query.filter_by(uid = uid).first()
        user.pin = pin
        user.adrress = adrress
        user.mobileno = phoneno

        db.session.commit()

        return redirect("/checkout")
    
    return render_template("orderInfopage.html",user = user)

@app.route("/userOrderList")
def userorderlist():
    if 'uid' not in session:
        # User is not logged in, redirect to the login page
        return redirect("/login")
    uid = session['uid']

    order = OrderItems.query.filter_by(user_id=uid).all()
    return render_template("OrderList.html",orders = order)

@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email,password = password).first()
        if user:
            session['name'] = user.name
            session['uid'] = user.uid
            session['email'] = user.email
            
            return redirect("/")
        else:
            render_template("login.html")
    return render_template("login.html")


@app.route("/logout")
def logout():
    # Clear the user_id from the session to indicate the user is logged out
    session.pop("name",None)
    session.pop("email",None)
    session.pop('uid', None)
    return redirect("/")
# -----------------------Product-------------------------------

@app.route("/product/ghahgovahguaflknfsahfl/<string:id>")
def productVeiw(id):
    product = Product.query.filter_by(pID = id).first()
    products = Product.query.all()

    if "uid" in session:
        uid = session['uid']
        alreadyInCart = CartItem.query.filter_by(user_id = uid,product_id = id).first()
    else:
        alreadyInCart = False 

   
    return render_template("productData.html",product = product,products = products,alreadyInCart = alreadyInCart)



@app.route("/addtocart/<int:pID>/<int:quant>")
def addtocart(pID,quant):
    product = Product.query.filter_by(pID = pID).first()

    if not(product):
        return "product not fond"
    
    if 'uid' not in session:
        # User is not logged in, redirect to the login page
        return redirect("/login")
    uid = session['uid']

    total = quant*int(product.sellingPrice)

    cart = CartItem(product_id = pID,user_id = uid,quantity  = quant,total = total,pname = product.name)
    db.session.add(cart)
    db.session.commit()

    cartitem = CartItem.query.filter_by(product_id = pID,user_id = uid).all()


    return redirect(f"/product/ghahgovahguaflknfsahfl/{product.pID}")
    

@app.route("/cart")
def cart():
    if 'uid' not in session:
        # User is not logged in, redirect to the login page
        return redirect("/login")
    uid = session['uid']

    cartitem = CartItem.query.filter_by(user_id = uid).all()

    return render_template("cart.html",cartitem = cartitem)

@app.route("/delete/<int:id>")
def delete_cart_items(id):
    cart_items = CartItem.query.filter_by(id=id).first()

    db.session.delete(cart_items)

    db.session.commit()
    return redirect("/cart")
   

# ------------------Order--------------------------------

@app.route("/checkout")
def checkout():
    if 'uid' not in session:
        # User is not logged in, redirect to the login page
        return redirect("/login")
    uid = session['uid']
    cartitem = CartItem.query.filter_by(user_id = uid).all()

    totalAmount = 0
    for item in cartitem:
        totalAmount = totalAmount+item.total

    # Create the Razorpay payment order and redirect to checkout page
    client = razorpay.Client(auth=("rzp_test_Zjom8IGzUOcgy1", "QTCPiD4BPPLsHcVtSN3DsUe4"))
    data = {"amount": totalAmount * 100, "currency": "INR", "receipt": f"{uid}"}
    payment = client.order.create(data=data)
    return render_template("payment.html",payment = payment)


@app.route("/order")
def order():
    if 'uid' not in session:
        # User is not logged in, redirect to the login page
        return redirect("/login")
    
    uid = session['uid']
    cart_items = CartItem.query.filter_by(user_id=uid).all()
    
    total_amount = sum(item.total for item in cart_items)

    # Create a new order
    order = Order(user_id=uid, totalAmount=total_amount, status="Order Placed")
    db.session.add(order)
    db.session.commit()

    # Add order items to the order
    for item in cart_items:
        order_item = OrderItems(
            product_id=item.product_id,
            product_name = item.pname,
            user_id = item.user_id ,
            order_id=order.orderId,
            quantity=item.quantity,
            subtotal=item.total,
            orderDate=datetime.now(indian_timezone)
        )
        db.session.add(order_item)

    # Clear the user's cart after placing the order
    CartItem.query.filter_by(user_id=uid).delete()
    db.session.commit()

    return "Order placed successfully!"






#-------------------Admin Code-------------------------

ad = 'admin'
ps = 'password'

@app.route("/adminlogin",methods=['GET','POST'])
def adminLogin():
    if request.method == 'POST':
        admin = request.form['admin']
        password = request.form['password']
        print(admin == ad and password == ps)
        if admin == ad and password == ps:
            return redirect("/adminhome")
    return render_template("adminLogin.html")


@app.route("/adminhome")
def adminHome():
    orders = Order.query.all()
    return render_template('AdminPage.html',orders = orders)

@app.route("/addProduct",methods = ['GET','POST'])
def addProduct():
    if request.method =='POST':
        name = request.form['name']
        mrp = request.form['mrp']
        sellingPrice = request.form['sellingPrice']
        file = request.files['file']
        tabDescription = request.form['tabDescription']
        stock = request.form['stock']
        mrp = int(mrp)
        sellingPrice = int(sellingPrice)
        discount = int(((mrp - sellingPrice)/mrp)*100)

        next_pID = (Product.query.count())+1
        filename =  f"{next_pID}.png"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        
        product = Product(name = name,mrp = mrp,sellingPrice = sellingPrice,imgurl = filename,tabDescription = tabDescription,stock = stock,discount = discount)
        db.session.add(product)
        db.session.commit()
        return render_template("ProductAdd.html")


    return render_template("ProductAdd.html")

@app.route("/updateProduct/<int:id>",methods=['GET','POST'])
def updateProduct(id):
    product = Product.query.filter_by(pID = id).first()
    if request.method =='POST':
        product.name = request.form['name']
        mrp = request.form['mrp']
        sellingPrice = request.form['sellingPrice']
        product.imgurl = request.form['imgurl']
        product.tabDescription = request.form['tabDescription']
        product.stock = request.form['stock']
        product.mrp = int(mrp)
        product.sellingPrice = int(sellingPrice)
        product.discount = int(((int(mrp) - int(sellingPrice))/int(mrp))*100)
        
        db.session.commit()

        return render_template("updateProduct.html",product = product)
      
    return render_template("updateProduct.html",product = product)


@app.route("/AdminListProducts")
def productList():
    product = Product.query.all()
    return render_template("UpdatePage.html",products = product)

# @app.route("/getOrderDetail/<int:oid>/<int:uid>")
# def orderDetails(oid,uid):
    
# @app.route("/delete")
# def delete_cart_items():
#     cart_items = CartItem.query.all()

#     for cart_item in cart_items:
#         db.session.delete(cart_item)

#     db.session.commit()

#     return "Delete successful"

import decimal

from flask import render_template, flash, request, redirect, url_for, session
from project.data import testimonials, branches, categorys
from project.model import Product, Order
from project.forms import CheckoutForm, LoginForm
from project import app, db
from datetime import datetime

testimonials = testimonials()
branches = branches()
categorys = categorys()
#-------------------------  Heading -------------------------
#
#-------------------------  Home -------------------------#

@app.route('/')
@app.route('/home/')
def home():
    return render_template('index.html', testimonials = testimonials, branches= branches)

@app.route('/category/')
def shop():
    return render_template('shop.html', categorys = categorys)

#------------------------- End Home -------------------------#
#
#-------------------------  Cart -------------------------#

@app.route('/cart')
def cart() :
    if "cart" not in session:
        return render_template('cart.html', cartItem = [], total = 0)
    else:
        items = session["cart"]
        cart_Items = []
        total_price = 0
        for item in items:
            product_item = Product.query.filter_by(id=item).first()
            cart_Items.append(product_item)
            total_price += product_item.cost
        return render_template('cart.html', cartItem = cart_Items, total = "₹ "+currencyInIndiaFormat(total_price))

@app.route('/add_to_cart/<product_name>')
def add_to_cart(product_name) :
    if Product.query.filter_by(name=product_name).first():
        new_product = Product.query.filter_by(name=product_name).first()
        if "cart" not in session:
            session["cart"] = []
        if new_product.id not in session["cart"]:
            session["cart"].append(new_product.id)
            session["len"] = len(session["cart"])
            session.modified = True
            flash(f'{new_product.name} is added to cart', 'success')
        else :
            flash(f'{new_product.name} is already in cart', 'info')
        return redirect(url_for('products', product_type=new_product.type))
    return redirect(url_for('invalid_address'))

@app.route('/empty_cart/<product_name>')
def empty_cart(product_name) :
    if "cart" in session:
        session.pop("cart", None)
        session.pop("len", None)
        flash(f'Cart is empty', 'danger')
    if product_name == 'cart':
        return redirect(url_for('cart'))
    if Product.query.filter_by(name=product_name).first():
        current_product = Product.query.filter_by(name=product_name).first()
        return redirect(url_for('product', product_type = current_product.type ,product_name= current_product.name))
    return redirect(url_for('invalid_address'))

@app.route('/delete_cart/<product_name>')
def delete_cart(product_name) :
    if Product.query.filter_by(name=product_name).first():
        delete_product = Product.query.filter_by(name=product_name).first()
        if "cart" in session:
            if delete_product.id in session["cart"]:
                if session["len"] < 2:
                    session.pop("cart", None)
                    session.pop("len", None)
                    flash(f'Cart is empty', 'danger')
                else:
                    session["cart"].remove(delete_product.id)
                    session["len"] = len(session["cart"])
                    flash(f'{delete_product.name} is removed', 'danger')
            else:
                flash(f'{delete_product.name} is removed', 'danger')

        return redirect(url_for('cart'))
    return redirect(url_for('invalid_address'))

#------------------------- End Cart -------------------------#
#
#-------------------------  Order -------------------------#

@app.route('/checkout/', methods=['POST','GET'])
def checkout() :
    form = CheckoutForm()
    if "cart" not in session:
        return render_template('cart.html', cartItem=[], total=0)
    items = session["cart"]
    cart_Items = []
    totalcost = 0
    for item in items:
        product_item = Product.query.filter_by(id=item).first()
        cart_Items.append(product_item)
        totalcost += product_item.cost
    if form.validate_on_submit():
        newOrder = Order(name=form.name.data,email=form.email.data, address=form.address.data, totalcost=totalcost, displayCost = "₹ "+currencyInIndiaFormat(totalcost) ,date_of_order=datetime.now())
        db.session.add(newOrder)
        for item in cart_Items:
            newOrder.product_id.append(item)
        db.session.commit()
        session.pop("cart", None)
        session.pop("len", None)
        return redirect(url_for('report', order_id= Order.query.all()[-1].id))
    return render_template('checkout.html', cartItem= cart_Items, form = form, cost = "₹ "+currencyInIndiaFormat(totalcost))

@app.route('/order/<int:order_id>')
def order_details(order_id) :
    if "user" not in session:
        return redirect(url_for('login'))
    if Order.query.filter_by(id=order_id).first():
        order_details = Order.query.filter_by(id=order_id).first()
        return render_template('order_details.html', order = order_details)
    return redirect(url_for('invalid_address'))

@app.route('/orders/')
def orders() :
    if "user" not in session:
        return redirect(url_for('login'))
    order_details = Order.query.all()
    return render_template('orders.html', orders = order_details, l = len(order_details))



@app.route('/buy_product/<product_name>')
def buy_product(product_name) :
    if Product.query.filter_by(name=product_name).first():
        new_product = Product.query.filter_by(name=product_name).first()
        if "cart" not in session:
            session["cart"] = []
        if new_product.id not in session["cart"]:
            session["cart"].append(new_product.id)
            session["len"] = len(session["cart"])
            session.modified = True
            flash(f'{new_product.name} is added to cart', 'success')
        else :
            flash(f'{new_product.name} is already in cart', 'info')
        return redirect(url_for('cart'))
    return redirect(url_for('invalid_address'))


@app.route('/report/<int:order_id>')
def report(order_id) :
    if Order.query.filter_by(id=order_id).first():
        order_details = Order.query.filter_by(id=order_id).first()
        return render_template('report.html', order=order_details)
    return redirect(url_for('invalid_address'))
#------------------------- End Order -------------------------#
#
#-------------------------  Product -------------------------#

@app.route('/product/<product_type>')
def products(product_type):
    if Product.query.filter_by(type=product_type).first():
        return render_template('products.html',products = Product.query.filter_by(type=product_type), product_type= str(product_type).capitalize())
    return redirect(url_for('invalid_address'))

@app.route('/product/<product_type>/<product_name>')
def product(product_type, product_name) :
    if Product.query.filter_by(type=product_type).first():
        if Product.query.filter_by(name=product_name).first():
            return render_template('product.html', product_details = Product.query.filter_by(name=product_name).first())
        return redirect(url_for('invalid_address'))
    return redirect(url_for('invalid_address'))

#------------------------- End Product -------------------------#
#
#-------------------------  Footer -------------------------#

@app.route('/aboutus/')
def aboutus() :
    return render_template('aboutus.html', )
#------------------------- End Footer -------------------------#
#
#-------------------------  Login -------------------------#

@app.route('/login/', methods=['POST','GET'])
def login() :
    form = LoginForm()
    if "user" in session:
        return redirect(url_for('orders'))
    if form.validate_on_submit():
        if form.un.data == "Admin" and form.pw.data =="admin":
            session["user"] = [form.un.data, form.pw.data]
            return redirect(url_for('orders'))
    return render_template('login.html', form= form)

@app.route('/logout/', methods=['POST','GET'])
def logout() :
    if "user" not in session:
        return redirect(url_for('login'))
    else:
        session.pop("user", None)
        return redirect(url_for('login'))


#------------------------- End Login -------------------------#
#
#-------------------------  Invalid -------------------------#

@app.errorhandler(404)
def invalid(txt):
    txt = "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
    return render_template('invalid.html',text = txt)

@app.route('/invalid_address/')
def invalid_address():
    txt = "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
    return render_template('invalid.html',text = txt)




def currencyInIndiaFormat(n):
  d = decimal.Decimal(str(n))
  if d.as_tuple().exponent < -2:
    s = str(n)
  else:
    s = '{0:.2f}'.format(n)
  l = len(s)
  i = l-1;
  res = ''
  flag = 0
  k = 0
  while i>=0:
    if flag==0:
      res = res + s[i]
      if s[i]=='.':
        flag = 1
    elif flag==1:
      k = k + 1
      res = res + s[i]
      if k==3 and i-1>=0:
        res = res + ','
        flag = 2
        k = 0
    else:
      k = k + 1
      res = res + s[i]
      if k==2 and i-1>=0:
        res = res + ','
        flag = 2
        k = 0
    i = i - 1

  return res[::-1]

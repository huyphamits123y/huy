from flask import  render_template, request, redirect, session, jsonify
import dao
from gkwebs import app, admin, login
from gkwebs import utils
from flask_login import login_user, logout_user, login_required
import cloudinary.uploader
from flask_login import current_user
from gkwebs.decorators import anonymous_user


@app.route("/")

def hello():
    products = dao.load_products(category_id=request.args.get("category_id"),
                                 kw=request.args.get('keyword'))
    return render_template('index.html', products=products)
@app.route("/products")
def product_list():
    category_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    products = utils.load_products( category_id=category_id, kw = kw, from_price = from_price, to_price = to_price)
    return render_template("products.html", products=products)

@app.route('/login-admin', methods=['post'])
def login_admin():
    username=request.form['username']
    password=request.form['password']
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')

@app.context_processor
def common_attributes():
    categories = dao.load_categories()
    return {
        'categories' : categories
    }
@app.route('/api/pay')
@login_required
def pay():
    key = app.config['CART_KEY']
    cart = session.get(key)
    if cart and dao.save_receipt(cart):
        del session[key]
    else:
        return jsonify({'status': 500})
    return jsonify({'status':200})
@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')
@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = dao.get_product_by_id(product_id)
    return render_template('product_detail.html', product=product)
@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=password,
                             avatar=avatar)

                return redirect('/login')
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)

@app.route('/cart')
def cart():
    # session['cart'] = {
    #     "1" : {
    #         "id":"1",
    #         "name": "iPhone 13",
    #         "price":12000,
    #         "quantity": 2
    #     },
    #     "2": {
    #         "id": "2",
    #         "name": "iPhone 14",
    #         "price": 15000,
    #         "quantity": 1
    #     },
    # }
    return render_template('cart.html')

@app.route('/api/cart', methods=['post'])
def add_to_cart():
    data = request.json
    key = app.config['CART_KEY']
    cart = session[key] if key in session else{}
    id = str(data['id'])
    name = data['name']
    price = data['price']
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id]={
            "id":id,
            "name": name,
            "price":price,
            "quantity": 1
        }
    session[key]=cart

    return jsonify(utils.cart_stats(cart))
@app.route('/login', methods=['get', 'post'])
@anonymous_user
def login_my_user():

    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username=username, password=password)
        if user:

            login_user(user=user)
            n = request.args.get("next")
            return redirect(n if n else '/')
    return render_template('login.html')
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id((user_id))
if __name__ == '__main__':
    app.run(debug=True)

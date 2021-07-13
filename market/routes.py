from sqlalchemy.orm import relation
from market import app
from flask import render_template,request,redirect, flash, url_for
from market.models import Item, User
from sqlalchemy.exc import IntegrityError
from market import db
from market.forms import RegisterForm, LoginForm    
from flask_login import login_user,logout_user, login_required, current_user

@app.route('/')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                            email=form.email.data, 
                            password=form.password.data,)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account Created successfully! Login successfully You are now loggedin as {user_to_create.username}',category='success')
        return redirect(url_for('market_page'))

    if form.errors != {}: #if there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user {err_msg} ', category='danger')


    return render_template('register.html', form=form)

@app.route('/login', methods=[ 'GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('market_page'))
    form = LoginForm()
    if form.validate_on_submit():
        attemted_user = User.query.filter_by(username = form.user.data).first()
        if attemted_user == None:
            attemted_user = User.query.filter_by(email = form.user.data).first()
        if attemted_user and attemted_user.check_password_correction(attempted_password = form.password.data):
            login_user(attemted_user)
            flash(f'Success! You are logged in as: {attemted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password are not match! Please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))


@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    quantity = 0
    total_price = 0
    confirm=False
    if request.method == 'POST':
        quantity = int(request.form['stocks'])
        item = Item.query.filter_by(id = request.form['purchased_item']).first()
        if quantity > int(item.stock):
            flash(f"Only {item.stock} number of items are available!", category="warning")
        else:
            confirm = True
            total_price = quantity * int(item.price)

    items = Item.query.all()
    return render_template('market.html', items = items, confirm=confirm, quantity = quantity, total_price = total_price)



@app.route('/become_a_seller')
@login_required
def become_a_seller():
    return render_template('become_a_seller.html')



@app.route('/add_item' , methods=['GET', 'POST'])
def add_item():
    message =""
    table_show = "true"
    if request.method == 'POST':
        try:
            pr_name = request.form['product_name']
            pr_barc = request.form['product_barc']
            pr_desc = request.form['product_desc']
            pr_price = request.form['product_price']
            pr_stock = request.form['product_stock']
            item = Item(name=pr_name, price=pr_price, barcode=pr_barc, description=pr_desc, stock=pr_stock)
            db.session.add(item)
            db.session.commit()
            message = "success"
            table_show = "true"

        except IntegrityError:
            db.session.rollback()
            message = "same_item"
            table_show = "true"

    products = Item.query.all()
    if len(products) == 0:
        table_show = "false"
        message = "danger"
    return render_template('additem.html', products=products, message=message, table_show=table_show)

@app.route("/delete_row/<int:id>")
def delete_row(id):
    del_row = Item.query.filter_by(id=id).first()
    db.session.delete(del_row)
    db.session.commit()
    return redirect(url_for('add_item'))

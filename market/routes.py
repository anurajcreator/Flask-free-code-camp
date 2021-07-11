from sqlalchemy.orm import relation
from market import app
from flask import render_template,request,redirect
from flask.helpers import url_for
from market.models import Item
from sqlalchemy.exc import IntegrityError
from market import db
from market.forms import RegisterForm


@app.route('/')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items = items)

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

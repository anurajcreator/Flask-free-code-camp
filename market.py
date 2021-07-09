from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)



@app.route('/')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]
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
            item = Item(name=pr_name, price=pr_price, barcode=pr_barc, description=pr_desc)
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


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)

from market import routes, models
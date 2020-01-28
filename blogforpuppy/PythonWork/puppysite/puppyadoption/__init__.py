import os
from flask import Flask,redirect,render_template,\
    flash,session,Blueprint,url_for,abort,request

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import FormField,StringField, SubmitField,IntegerField, PasswordField, ValidationError
from wtforms.validators import DataRequired, email, EqualTo
from flask_login import LoginManager, UserMixin, login_user,login_required,logout_user
from werkzeug.security import generate_password_hash,check_password_hash


login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login'

from puppyadoption.puppies.views import puppies_blueprint
from puppyadoption.owners.views import owners_blueprint

app.register_blueprint(owners_blueprint,url_prefix='/owners')
app.register_blueprint(puppies_blueprint,url_prefix='/puppies')
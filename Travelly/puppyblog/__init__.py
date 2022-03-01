import os
from flask import Flask,redirect,render_template,\
    flash,session,Blueprint,url_for,abort,request, current_app

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import FormField,StringField, SubmitField,IntegerField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, email, EqualTo,Email,ValidationError
from flask_login import LoginManager, UserMixin, login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask_wtf.file import FileField,FileAllowed
from PIL import Image


login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db,render_as_batch=True)

login_manager.init_app(app)
login_manager.login_view = 'users.login'





from puppyblog.core.views import core
from puppyblog.error_pages.handlers import error_pages
from puppyblog.users.views import users_blueprint
from puppyblog.blog_posts.views import blog_posts
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users_blueprint)
app.register_blueprint(blog_posts)
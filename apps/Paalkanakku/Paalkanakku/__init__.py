import os
from flask import Flask, redirect, render_template, url_for
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


import gspread
try:
    from Paalkanakku.errors_pages.handlers import error_pages
    #from Paalkanakku.config import cred_filename, client_secrets, google_blueprint
except:
    from Paalkanakku.Paalkanakku.config import cred_filename, client_secrets
    from Paalkanakku.Paalkanakku.errors_pages.handlers import error_pages
    #from Paalkanakku.Paalkanakku.config import google_blueprint


app = Flask(__name__)


############################
###DATABASE Setup
###########################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

app.secret_key = 'super secret key'
########################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


try:
    from Paalkanakku.customers.views import customer
    from Paalkanakku.users.views import users
    from Paalkanakku.core.views import core
except:
    from Paalkanakku.Paalkanakku.customers.views import customer
    from Paalkanakku.Paalkanakku.users.views import users
    from Paalkanakku.Paalkanakku.core.views import core


app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(customer)
app.register_blueprint(error_pages)
#app.register_blueprint(google_blueprint, url_prefix="/login")
#gcc = gspread.oauth(credentials_filename=cred_filename)















"""import gspread


cred_filename = "/home/alexanders/Documents/Python/Local_Copy/Localgit/Google/google_apps/MoiKanakku/Moikanakku" \
                "/moikanakku-341816-5b7d7ef75ff9.json"
file_name = "Aruna Swetha Sadangu"


gc = gspread.service_account(filename=cred_filename)

#sheet = gc.open(file_name).sheet1

#sheet = client.open("Aruna Swetha Sadangu").sheet1
#total_rows = str(sheet.row_count)

#data = sheet.get('A1:H'+total_rows)"""
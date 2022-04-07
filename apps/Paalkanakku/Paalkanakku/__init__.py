import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import MetaData

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
#app.config["SQLALCHEMY_ECHO"] = True

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)

Migrate(app, db, render_as_batch=True)

app.secret_key = 'super secret key'
########################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
app.config['RECAPTCHA_OPTIONS']= {'theme':'dark'}

from Paalkanakku.milkdata.views import milk
try:
    from Paalkanakku.customers.views import customer
    from Paalkanakku.users.views import users
    from Paalkanakku.core.views import core
    from Paalkanakku.owner.views import owner
    from Paalkanakku.milkers.views import milker


except:
    from Paalkanakku.Paalkanakku.customers.views import customer
    from Paalkanakku.Paalkanakku.users.views import users
    from Paalkanakku.Paalkanakku.core.views import core
    from Paalkanakku.Paalkanakku.milkers.views import milker
    from Paalkanakku.Paalkanakku.owner.views import owner
    from Paalkanakku.Paalkanakku.milkdata.views import milk




app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(customer)
app.register_blueprint(milker)
app.register_blueprint(owner)
app.register_blueprint(milk)
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
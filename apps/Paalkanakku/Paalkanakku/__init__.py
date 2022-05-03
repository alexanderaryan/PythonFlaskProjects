import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import MetaData
from datetime import datetime
from flask_crontab import Crontab

try:
    from Paalkanakku.errors_pages.handlers import error_pages
    #from Paalkanakku.config import cred_filename, client_secrets, google_blueprint
except:
    from Paalkanakku.Paalkanakku.config import cred_filename, client_secrets
    from Paalkanakku.Paalkanakku.errors_pages.handlers import error_pages
    #from Paalkanakku.Paalkanakku.config import google_blueprint


today_date = datetime.date(datetime.today())

app = Flask(__name__)
crontab = Crontab(app)

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


app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI' #Key generated from google API. 1 Million hit per month
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe' #6LcDM4YfAAAAABUHmHnvUbpPxS7-rTJLlCDPsyR4
app.config['RECAPTCHA_OPTIONS']= {'theme':'dark'}

try:
    from Paalkanakku.customers.views import customer
    from Paalkanakku.users.views import users
    from Paalkanakku.core.views import core
    from Paalkanakku.owner.views import owner
    from Paalkanakku.milkers.views import milker
    from Paalkanakku.milkdata.views import milk

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

from flask import Flask,render_template,redirect,Blueprint,url_for,request,session,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, FormField, FieldList, Form, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget,CheckboxInput
from wtforms.fields.html5 import DateField
import os
from flask_dance.contrib.google import make_google_blueprint,google
import flask_dance

app = Flask(__name__)

app.config['SECRET_KEY']="mysecretkey"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'

google_blueprint = make_google_blueprint(client_id='1069073817725-vsujpd8i576fjda35g9ruku9ssigrree.apps.googleusercontent.com',
                                         client_secret='SgLjmeyvjXIiTnf4asy_9IxR',
                                         offline = True,scope=['profile','email'])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tour')
def tour():
    return render_template('tour.html')

@app.route('/login')
def login():
    if not google.authorized:
        return render_template(url_for('google.login'))
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text

    email = resp.json()['email']

    return email

from dressme.attireshuffler.views import dress_print
app.register_blueprint(dress_print)
app.register_blueprint(google_blueprint,url_prefix='/login')
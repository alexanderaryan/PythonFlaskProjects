from flask import Flask,render_template,redirect,Blueprint,url_for,request,session
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, FormField, FieldList, Form, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget,CheckboxInput
from wtforms.fields.html5 import DateField

app = Flask(__name__)

app.config['SECRET_KEY']="mysecretkey"
@app.route('/')
def index():
    return render_template('index.html')

from dressme.attireshuffler.views import dress_print
app.register_blueprint(dress_print)
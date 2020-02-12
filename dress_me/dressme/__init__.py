from flask import Flask,render_template,redirect,Blueprint,url_for,request,session
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, FormField, FieldList, Form
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY']="mysecretkey"
@app.route('/')
def index():
    return render_template('index.html')

from dress_me.dressme.attireshuffler.views import dress_print
app.register_blueprint(dress_print)
from flask import render_template, request, Blueprint

customer = Blueprint('customer',__name__)


@customer.route('/add')
def index():
    return render_template('index.html')


@customer.route('/remove')
def info():
    return render_template('info.html')


@customer.route('/list')
def list_cust():
    return render_template('info.html')

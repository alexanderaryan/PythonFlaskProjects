from flask import render_template, request, Blueprint

customer = Blueprint('customer',__name__)


@customer.route('/add')
def add_cust():
    return render_template('info.html')


@customer.route('/remove')
def remove_cust():
    return render_template('info.html')


@customer.route('/list')
def list_cust():
    return render_template('info.html')

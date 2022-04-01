from flask import render_template, request, Blueprint
from datetime import datetime

core = Blueprint('core',__name__)


@core.route('/')
def index():
    # More to come
    return render_template('index.html')


@core.route('/info')
def info():
    return render_template('info.html')

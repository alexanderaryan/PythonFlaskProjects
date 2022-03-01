from flask import Flask, redirect, render_template, session, flash
import os
from Moikanakku.moi_sheet_import import data, header, card, moi_data_l, moi_data_s,\
    moi_data_by_name_l, moi_data_by_name_s


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


@app.route('/img', methods=['GET', 'POST'])
def images():
    img_list = os.listdir('static/Images')
    img_count = len(img_list)
    return render_template("images.html", img_count=img_count, img_list=img_list)


@app.route('/charts', methods=['GET', 'POST'])
def charts():
    return render_template(
        "charts.html",
        moi_data_l=moi_data_l,
        moi_data_s=moi_data_s,
        moi_data_by_name_l=moi_data_by_name_l,
        moi_data_by_name_s=moi_data_by_name_s
    )


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", card=card)


@app.route('/ledger')
def ledger():
    return render_template("ledger.html", header=header, data=data)


if __name__ == '__main__':
    app.run(debug=True)

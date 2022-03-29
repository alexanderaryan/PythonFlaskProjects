from Paalkanakku.milkdata.forms import AddDailyData, DailyData
try:
    from Paalkanakku import app, db
    from Paalkanakku.models import Milkers, CowOwner, Milk

except:
    from Paalkanakku.Paalkanakku import app, db
    from Paalkanakku.Paalkanakku.models import Milkers, CowOwner, Milk
    from Paalkanakku.Paalkanakku.milkdata.forms import AddDailyData, DailyData

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

milk = Blueprint('milk', __name__)


@milk.route('/daily',methods=["GET","POST"])
@login_required
def add_daily_data():

    form = AddDailyData()

    customer_set =  (CowOwner.query.with_entities(CowOwner.owner_id,CowOwner.name,CowOwner.place).\
           filter(CowOwner.milker_id.in_(DailyData.milker_ids)).group_by(CowOwner.place,CowOwner.owner_id,CowOwner.name).\
           order_by(CowOwner.place,CowOwner.name).all())

    print(form.daily_data, "Printing form")

    #print (customer_set,milkers)
    print(form.form_errors)
    print(form.data, "data of form")

    print (form.validate_on_submit())
    if form.validate_on_submit():
        print (form.daily_data.data)
        for each_cust in form.daily_data:
            milk_data=Milk(
                owner_id=each_cust.owner_id.data,
                milker=each_cust.milker.data,
                milked_date=form.milked_date.data,
                milked_time=each_cust.milked_time.data,
                litre=each_cust.litre.data,
                ml=each_cust.ml.data
            )
            db.session.add(milk_data)
        print ("committing")
        db.session.commit()
        print("committed")

    daily_data_form = DailyData()
    milk_header = [daily_data_form.owner_id.label,daily_data_form.cust_name.label, daily_data_form.place.label, daily_data_form.milker.label,
                   daily_data_form.milked_time.label,
                   daily_data_form.litre.label,
                   daily_data_form.ml.label]
    header = milk_header

    return render_template('milk/daily_data.html',
                           form=form,
                           header=header,
                           customer_set=customer_set,
                           flash=flash)


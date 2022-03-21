try:
    from Paalkanakku import app, db
    from Paalkanakku.models import Milkers, CowOwner, Milk
    from Paalkanakku.milkdata.forms import AddDailyData

except:
    from Paalkanakku.Paalkanakku import app, db
    from Paalkanakku.Paalkanakku.models import Milkers, CowOwner, Milk
    from Paalkanakku.Paalkanakku.milkdata.forms import AddDailyData

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

milk = Blueprint('milk', __name__)


@milk.route('/daily',methods=["GET","POST"])
@login_required
def add_daily_data():

    form = AddDailyData()

    milker_data = Milkers.query.all()
    milker_ids = [milker.milker_id for milker in milker_data]
    customer_set =  (CowOwner.query.with_entities(CowOwner.owner_id,CowOwner.name,CowOwner.place).\
           filter(CowOwner.milker_id.in_(milker_ids)).group_by(CowOwner.place,CowOwner.owner_id,CowOwner.name).\
           order_by(CowOwner.place,CowOwner.name).all())

    milkers = [(milker.milker_id, milker.name) for milker in milker_data]
    form.milker.choices = milkers

    #print (customer_set,milkers)
    print(form.form_errors)
    print(form.data, "data of form")

    print (form.validate_on_submit())
    if form.validate_on_submit():
        milk_data=Milk(
            owner_id=form.owner_id.data,
            milker=form.milker.data,
            milked_date=form.milked_date.data,
            milked_time=form.milked_time.data,
            litre=form.litre.data,
            ml=form.ml.data
        )
        db.session.add(milk_data)
        print ("committing")
        db.session.commit()
        print("committed")

    header = [form.name.label, form.place.label,form.milker.label,form.milked_time.label,form.litre.label,form.ml.label]

    return render_template('milk/daily_data.html',
                           form=form,
                           header=header,
                           customer_set=customer_set,
                           flash=flash)


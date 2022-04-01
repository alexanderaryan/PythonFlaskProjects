from datetime import datetime


try:
    from Paalkanakku import app, db
    from Paalkanakku.models import Milkers, CowOwner, Milk
    from Paalkanakku.milkdata.forms import AddDailyData, DailyData
except:
    from Paalkanakku.Paalkanakku import app, db
    from Paalkanakku.Paalkanakku.models import Milkers, CowOwner, Milk
    from Paalkanakku.Paalkanakku.milkdata.forms import AddDailyData, DailyData

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

milk = Blueprint('milk', __name__)


def milk_data_check(date):

    day = datetime(date.year,date.month,date.day)
    #today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    #milk_data = Milk.query.filter(Milk.milked_date.in_(datetime.today())).first()
    #milk_data = Milk.query.with_entities(Milk.milked_date).first()
    milk_data = Milk.query.filter(Milk.milked_date == day).all()
    print ("sd",milk_data)
    return milk_data


@milk.route('/daily/<modified_day>',methods=["GET","POST"])
@login_required
def add_daily_data(modified_day=None):

    form = AddDailyData()

    print ("Modified_day",modified_day,type(modified_day))
    customer_set =  (CowOwner.query.with_entities(CowOwner.owner_id,CowOwner.name,CowOwner.place).\
           filter(CowOwner.milker_id.in_(DailyData.milker_ids)).group_by(CowOwner.place,CowOwner.owner_id,CowOwner.name).\
           order_by(CowOwner.place,CowOwner.name).all())

    print(form.daily_data, "Printing form")
    print (customer_set)

    if modified_day == "None":
        day = datetime.date(datetime.today())
        return redirect(url_for('milk.add_daily_data', modified_day=day))
    else:
        day = datetime.strptime(modified_day, '%Y-%m-%d').date()

    milk_data_for_today = milk_data_check(day)
    print ("buddhgsd",milk_data_for_today)
    for n in milk_data_for_today:
        print("milker", n.milker_id)

    #print (customer_set,milkers)
    print(form.form_errors)
    print(form.data, "data of form")

    print (form.validate_on_submit())
    if form.validate_on_submit():
        print ("inside form",milk_data_check(form.milked_date.data))
        milk_data = milk_data_check(form.milked_date.data)
        if not milk_data:
            print (form.daily_data.data)
            print (type(form.milked_date.data))
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
            return redirect(url_for('milk.add_daily_data',modified_day=form.milked_date.data))
        else:
            print ("Hello",form.data)
            for each in form.daily_data:
                for m in milk_data:
                    # print ('N',n.milker_id,n.owner_id,n.milked_time,n.litre,n.ml,n.milked_date)
                    if m.owner_id == each.owner_id.data:
                        print ("rim",each.milked_time.data)
                        print (each.milker.data)
                        m.milker_id=each.milker.data
                        m.milked_time = each.milked_time.data
                        m.litre = each.litre.data
                        m.ml = each.ml.data
                        print ("m",m)
                        db.session.add(m)
                    db.session.commit()
            print (form.milked_date.data)
            return redirect(url_for('milk.add_daily_data',modified_day=form.milked_date.data))

    daily_data_form = DailyData()
    milk_header = [daily_data_form.owner_id.label,
                   daily_data_form.cust_name.label,
                   daily_data_form.place.label,
                   daily_data_form.milker.label,
                   daily_data_form.milked_time.label,
                   daily_data_form.litre.label,
                   daily_data_form.ml.label]
    header = milk_header
    print ("days",modified_day,day)
    return render_template('milk/daily_data.html',
                           form=form,
                           day=day,
                           modified_day = modified_day,
                           header=header,
                           milk_data_for_today=milk_data_for_today,
                           customer_set=customer_set,
                           flash=flash)


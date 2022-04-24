from datetime import datetime, timedelta
from sqlalchemy import func
import yaml

try:
    from Paalkanakku import app, db
    from Paalkanakku.models import Milkers, CowOwner, Milk
    from Paalkanakku.milkdata.forms import AddDailyData, DailyData, LedgerView, milker_data
    from Paalkanakku.milkdata import google_backup
except:
    from Paalkanakku.Paalkanakku import app, db
    from Paalkanakku.Paalkanakku.models import Milkers, CowOwner, Milk
    from Paalkanakku.Paalkanakku.milkdata.forms import AddDailyData, DailyData
    from Paalkanakku.Paalkanakku.milkdata import google_backup


from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

milk = Blueprint('milk', __name__)

today_date = datetime.date(datetime.today())


def check_google_sheet():
    with open("/home/alexanders/Documents/Python/GitPythonWork/apps/Paalkanakku/Paalkanakku/config.yaml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)
        if data['gsheet_url'] is not None:
            print(data['gsheet_url'])
            sheet_url = data['gsheet_url']
            return sheet_url
        else:
            return False

def milk_data_check(date,milked_time):

    day = datetime(date.year,date.month,date.day)
    #today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    print("In",day,type(day))


    #milk_data = Milk.query.filter(Milk.milked_date.in_(datetime.today())).first()
    #milk_data = Milk.query.with_entities(Milk.milked_date).first()
    if milked_time == "am":
        milk_data = Milk.query.filter(Milk.milked_date == day).filter(Milk.am_litre != None).all()
    else:
        milk_data = Milk.query.filter(Milk.milked_date == day).filter(Milk.pm_litre!=None).all()
    print ("sd",milk_data)
    return milk_data


def price(date):

    """ To return the price of milk on a particular day"""

    day = datetime(date.year, date.month, date.day)
    print("out ",day,type(day))

    milk_data = Milk.query.with_entities(Milk.price).filter(Milk.milked_date == day).first()
    if not milk_data:
        milk_data = Milk.query.with_entities(Milk.price,Milk.milked_date).order_by(Milk.milked_date.desc()).first()

    return milk_data[0] if milk_data is not None else "0.00"


class whole_month_data():

    def __init__(self,month):
        print("before",month)
        self.month = month
        self.first_day_of_month = datetime.combine(self.month, datetime.min.time())
        nxt_mnth = self.first_day_of_month.replace(day=28) + timedelta(days=4)
        print("dat", nxt_mnth.day)
        self.last_day_of_month = nxt_mnth - timedelta(days=nxt_mnth.day)
        print(self.last_day_of_month)
        print("after", self.last_day_of_month, self.first_day_of_month)

    def ledger_calc(self):
        """To return monthly legderdata"""

        milk_data = Milk.query.with_entities(Milk.owner_id,
                                             func.coalesce(func.sum(Milk.am_litre), 0.0).label('AM_Total'),
                                             func.coalesce(func.sum(Milk.pm_litre), 0.0).label('PM_Total'),
                        func.coalesce(func.sum(Milk.am_litre*Milk.price), 0.0).label('AM_Total_Price'),
                    func.coalesce(func.sum(Milk.pm_litre*Milk.price), 0.0).label('PM_Total_Price')).\
            filter(Milk.milked_date.between( self.first_day_of_month,self.last_day_of_month)).\
            group_by(Milk.owner_id).\
            order_by(Milk.owner_id).all()

        return milk_data

"""def milker_set():
    

    milker_data = Milkers.query.all()
    milker_ids = [milker.milker_id for milker in milker_data]
    milkers = [(milker.milker_id, milker.name) for milker in milker_data]

    return milkers,milker_ids"""


def customer_set(active=False):
    """
    To give the set of customers added in the Owners Table
    """
    milker_ids = milker_data()[1]
    try:
        if not active:
            customer =  (CowOwner.query.with_entities(CowOwner.owner_id,CowOwner.name,CowOwner.place).\
                   filter(CowOwner.milker_id.in_(milker_ids)).group_by(CowOwner.place,CowOwner.owner_id,CowOwner.name).\
                   order_by(CowOwner.place,CowOwner.name).all())
        else:
            customer = (CowOwner.query.with_entities(CowOwner.owner_id, CowOwner.name, CowOwner.place). \
                            filter(CowOwner.milker_id.in_(milker_ids),CowOwner.active==True).group_by(CowOwner.place, CowOwner.owner_id,
                                                                                CowOwner.name). \
                            order_by(CowOwner.place, CowOwner.name).all())
    except:
        print ('CowOwner table is empty')
        customer = None

    return customer


@milk.route('/daily/<modified_day>/<milked_time>',methods=["GET","POST"])
@login_required
def add_daily_data(modified_day=None,milked_time=None):

    form = AddDailyData()

    print (type(form.daily_data),len(form.daily_data))
    print(type(form.milked_time))
    print("Form", form.daily_data)
    print ("Modified_day",modified_day,type(modified_day))

    print(len(form.daily_data), "Printing form")

    if modified_day == "None":
        day = today_date
        milked_time = "am"
        rate = price(day)
        return redirect(url_for('milk.add_daily_data', modified_day=day,milked_time=milked_time))
    else:
        day = datetime.strptime(modified_day, '%Y-%m-%d').date()
        milked_time = milked_time
        print ("MilkedTime",milked_time)
        rate = price(day)



    if milked_time != "am":
        milk_data_for_today = milk_data_check(day,milked_time)
        print ("Form there",milked_time,milk_data_for_today)
    else:
        milk_data_for_today = milk_data_check(day, "am")
        print("Form not ", milk_data_for_today)
    print ("buddhgsd",milk_data_for_today)

    for n in milk_data_for_today:
        print("milker", n.milker_id,n.am_litre,n.pm_litre)
    if not milk_data_for_today:
        form.daily_data[0].milker.choices = milker_data(False)[2]
        print(milker_data(False)[2])
        customers = customer_set(True)
    else:
        form.daily_data[0].milker.choices = milker_data()[2]
        print(milker_data(False)[2])
        customers = customer_set()

    print("Length", len(customers), len(milk_data_for_today))
    #print (customer_set,milkers)

    print(form.data, "data of form")

    print ("Form validation is ",form.validate_on_submit())
    if form.validate_on_submit():
        print ("inside form",milk_data_check(form.milked_date.data,form.milked_time.data))
        milk_data = milk_data_check(form.milked_date.data,form.milked_time.data)
        if not milk_data:
            print (form.daily_data.data)
            print (type(form.milked_date.data))
            for each_cust in form.daily_data:
                milk_data=Milk(
                    owner_id=each_cust.owner_id.data,
                    milker=each_cust.milker.data,
                    milked_date=form.milked_date.data,
                    milked_time=form.milked_time.data,
                    litre=each_cust.litre.data,
                    ml=each_cust.ml.data,
                    price=form.price.data
                )
                db.session.add(milk_data)
            print ("committing")
            db.session.commit()
            print("committed")
            return redirect(url_for('milk.add_daily_data',modified_day=form.milked_date.data,milked_time=form.milked_time.data))
        else:
            print ("Hello",form.data)
            for each in form.daily_data:
                for m in milk_data:
                    # print ('N',n.milker_id,n.owner_id,n.milked_time,n.litre,n.ml,n.milked_date)
                    if m.owner_id == each.owner_id.data:
                        print ("rim",form.milked_time.data)
                        print (each.milker.data)
                        m.milker_id=each.milker.data
                        m.price=form.price.data
                        if form.milked_time.data == "am":
                            m.am_litre = Milk.litre_conv(m,each.litre.data,each.ml.data)
                        else:
                            m.pm_litre = Milk.litre_conv(m,each.litre.data, each.ml.data)
                        print("m", each.ml.data)
                        print ("m",m.am_litre)
                        db.session.add(m)
                    db.session.commit()
            print (form.milked_date.data)
            return redirect(url_for('milk.add_daily_data',modified_day=form.milked_date.data,milked_time=form.milked_time.data))

    for error,message in form.errors.items():
        flash(f"{error.capitalize()} : {message[0]}", category='error')


    daily_data_form = DailyData()
    milk_header = [daily_data_form.owner_id.label,
                   daily_data_form.place.label,
                   daily_data_form.cust_name.label,
                   daily_data_form.milker.label,
                   daily_data_form.litre.label,
                   daily_data_form.ml.label]
    header = milk_header
    print ("days", modified_day, day, milk_data_for_today, milked_time)
    for n in milk_data_for_today:
        print (n.milker_id, n.owner_id, n.am_litre, n.pm_litre)

    return render_template('milk/daily_data.html',
                           form=form,
                           day=day,
                           modified_day = modified_day,
                           header=header,
                           rate=rate,
                           milk_data_for_today=milk_data_for_today,
                           milked_time=milked_time,
                           customer_set=customers,
                           flash=flash)

"""from Paalkanakku import app, db
from Paalkanakku.models import Milkers, CowOwner, Milk
print (Milk.query.delete())
db.session.commit()"""




@milk.route('/ledger/<month>',methods=["GET","POST"])
@login_required
def milk_ledger_view(month=None):

    form = LedgerView()

    if month == "None":
        month = today_date.replace(day=1)
        print ("Here is te month",month)
        return redirect(url_for('milk.milk_ledger_view', month=month))
    else:
        month = datetime.strptime(month, '%Y-%m-%d').date()

    ledger_obj= whole_month_data(month)
    monthly_ledger = ledger_obj.ledger_calc()

    print("mon", type(month))
    print("data", monthly_ledger)
    #sheet_url = google_backup.spreadsheet_check(month.strftime("%Y")+"Paalkanakku").url
    sheet_url = "dumm"
    if check_google_sheet() is False:
        sheet_url = google_backup.spreadsheet_check(month.strftime("%Y") + "Paalkanakku").url
        yaml_data = {'gsheet_url' : sheet_url}
        print ("Sheet Not found")
        with open("/home/alexanders/Documents/Python/GitPythonWork/apps/Paalkanakku/Paalkanakku/config.yaml","w+") as w:
            data = yaml.dump(yaml_data, w)
    else:
        sheet_url = check_google_sheet()

    if form.validate_on_submit():
        print (form.month.data)
        monthly_ledger = ledger_obj.ledger_calc()
        print ("mon",form.month.data)
        print ("data",monthly_ledger)
        mon = google_backup.add_data_to_google(date_object=month,
                                         first=ledger_obj.first_day_of_month,
                                         last=ledger_obj.last_day_of_month)
        flash(f"The data is backed up for {mon}")
        return redirect(url_for("milk.milk_ledger_view", month=form.month.data))

    header = ['Place','Name','AM','PM','Total','AM Price','PM Price','Total Price']
    tm_header = ['ஊர்', 'பெயர்', 'காலை', 'மாலை', 'மொத்தம்', 'காலை விலை', 'மாலை விலை', 'மொத்த விலை']

    return render_template('milk/view_ledger.html',
                           form=form,
                           month=month,
                           tm_header = tm_header,
                           header=header,
                           monthly_ledger=monthly_ledger,
                           customer_set=customer_set(),
                           sheet_url=sheet_url)

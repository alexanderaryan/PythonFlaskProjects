from datetime import datetime, timedelta

from sqlalchemy import func
import yaml

try:
    from Paalkanakku import app, db, today_date, crontab
    from Paalkanakku.models import Milkers, CowOwner, Milk, Loan, LoanLedger
    from Paalkanakku.milkdata.forms import AddDailyData, DailyData, LedgerView, milker_data, loan_choice
    from Paalkanakku.owner.forms import LoanLedgerForm
    from Paalkanakku.milkdata import google_backup
    from Paalkanakku.config import sheet_config
except:
    from Paalkanakku.Paalkanakku import app, db, today_date, crontab
    from Paalkanakku.Paalkanakku.models import Milkers, CowOwner, Milk, Loan, LoanLedger
    from Paalkanakku.Paalkanakku.owner.forms import LoanLedgerForm
    from Paalkanakku.Paalkanakku.milkdata.forms import AddDailyData, DailyData, LedgerView, milker_data, loan_choice
    from Paalkanakku.Paalkanakku.milkdata import google_backup
    from Paalkanakku.Paalkanakku.config import sheet_config

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

milk = Blueprint('milk', __name__)


def check_google_sheet():
    with open(sheet_config) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)
        if data['gsheet_url'] is not None:
            print(data['gsheet_url'])
            sheet_url = data['gsheet_url']
            return sheet_url
        else:
            return False


def config_data():
    stream = open(sheet_config, 'r')
    data = yaml.load(stream, Loader=yaml.FullLoader)

    return data


milking_charge = config_data()['milking_charge']


def milk_data_check(date, milked_time):
    day = datetime(date.year, date.month, date.day)
    # today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    print("In", day, type(day))

    # milk_data = Milk.query.filter(Milk.milked_date.in_(datetime.today())).first()
    # milk_data = Milk.query.with_entities(Milk.milked_date).first()
    if milked_time == "am":
        milk_data = Milk.query.filter(Milk.milked_date == day).filter(Milk.am_litre != None).all()
    else:
        milk_data = Milk.query.filter(Milk.milked_date == day).filter(Milk.pm_litre != None).all()
    print("sd", milk_data)
    return milk_data


def price(date):
    """ To return the price of milk on a particular day"""

    day = datetime(date.year, date.month, date.day)
    print("out ", day, type(day))

    milk_data = Milk.query.with_entities(Milk.price).filter(Milk.milked_date == day).first()
    if not milk_data:
        milk_data = Milk.query.with_entities(Milk.price, Milk.milked_date).order_by(Milk.milked_date.desc()).first()

    return milk_data[0] if milk_data is not None else "0.00"


@app.context_processor
def utility_processor():
    def milk_price():
        return price(date=today_date)

    return dict(milk_price=milk_price)


class WholeMonthData:

    def __init__(self, month):
        print("before", month)
        self.month = month
        self.first_day_of_month = datetime.combine(self.month, datetime.min.time())
        nxt_mnth = self.first_day_of_month.replace(day=28) + timedelta(days=4)
        print("dat", nxt_mnth.day)
        self.last_day_of_month = nxt_mnth - timedelta(days=nxt_mnth.day)
        print(self.last_day_of_month)
        print("after", self.last_day_of_month, self.first_day_of_month)
        self.milk_data_query = Milk.query.with_entities(Milk.owner_id,
                                                        func.coalesce(func.sum(Milk.am_litre), 0.0).label('AM_Total'),
                                                        func.coalesce(func.sum(Milk.pm_litre), 0.0).label('PM_Total'),
                                                        func.coalesce(func.sum(Milk.am_litre * Milk.price), 0.0).label(
                                                            'AM_Total_Price'),
                                                        func.coalesce(func.sum(Milk.pm_litre * Milk.price), 0.0).label(
                                                            'PM_Total_Price'),
                                                        func.coalesce(func.sum(Milk.fodder), 0.0).label('Fodder'),
                                                        func.coalesce(func.sum(Milk.loan), 0.0).label('Loan'),
                                                        func.coalesce(func.sum(Milk.advance), 0.0).label('Advance'),
                                                        func.coalesce(func.sum(Milk.dr_service), 0.0).label(
                                                            'Dr_service')). \
            filter(Milk.milked_date.between(self.first_day_of_month, self.last_day_of_month))

    def ledger_calc(self):
        """To return monthly legderdata"""

        milk_data = self.milk_data_query.group_by(Milk.owner_id).order_by(Milk.owner_id).all()
        print("whole", milk_data)
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
            customer = (CowOwner.query. \
                        filter(CowOwner.milker_id.in_(milker_ids)).group_by(CowOwner.owner_id). \
                        order_by(CowOwner.place, CowOwner.name).all())
        else:
            customer = (CowOwner.query. \
                        filter(CowOwner.milker_id.in_(milker_ids), CowOwner.active == True).group_by(CowOwner.owner_id). \
                        order_by(CowOwner.place, CowOwner.name).all())
    except:
        print('CowOwner table is empty')
        customer = []

    return customer


@milk.route('/daily/<modified_day>/<milked_time>', methods=["GET", "POST"])
@login_required
def add_daily_data(modified_day=None, milked_time=None):

    form = AddDailyData()

    print(type(form.daily_data), len(form.daily_data))
    print(type(form.milked_time))
    print("Form", form.daily_data)
    form.daily_data[0].loan_id.choices=loan_choice()
    print("Modified_day", modified_day, type(modified_day))

    print(len(form.daily_data), "Printing form")

    if modified_day == "None":
        day = today_date
        milked_time = "am"
        rate = price(day)
        return redirect(url_for('milk.add_daily_data', modified_day=day, milked_time=milked_time))
    else:
        day = datetime.strptime(modified_day, '%Y-%m-%d').date()
        milked_time = milked_time
        print("MilkedTime", milked_time)
        rate = price(day)

    no_milker = config_data()['no_milker']
    print(no_milker, "milker")

    if milked_time != "am":
        milk_data_for_today = milk_data_check(day, milked_time)
        print("Form there", milked_time, milk_data_for_today)
    else:
        milk_data_for_today = milk_data_check(day, "am")
        print("Form not ", milk_data_for_today)
    print("buddhgsd", milk_data_for_today)

    loan_details = Loan.all_loan()
    print("Loan data", loan_details)

    owners_with_load = Loan.owners_with_loan()
    print (owners_with_load)
    for n in milk_data_for_today:
        print("milker", n.milker_id, n.am_litre, n.pm_litre)
    if not milk_data_for_today:
        if not no_milker:
            form.daily_data[0].milker.choices = milker_data(False)[2]
            print(milker_data(False)[2])
        customers = customer_set(True)
    else:
        if not no_milker:
            form.daily_data[0].milker.choices = milker_data()[2]
            print(milker_data(False)[2])
        customers = customer_set()

    # print("Length", len(customers), len(milk_data_for_today))
    print("customers", customers)
    print(form.data, "data of form")
    print("Form validation is ", form.validate_on_submit())

    if form.validate_on_submit():
        print ("Where")
        print([(f.loan_id.data, f.loan_amount.data) for f in form.daily_data], "Form")
        if form.milking_charge.data:
            data = config_data()
            print(data['milking_charge'])
            data['milking_charge'] = form.milking_charge.data

            with open(sheet_config, 'w') as yaml_file:
                yaml_file.write(yaml.dump(data, default_flow_style=False))

        print("inside form", milk_data_check(form.milked_date.data, form.milked_time.data))
        milk_data = milk_data_check(form.milked_date.data, form.milked_time.data)

        if not milk_data:
            print(form.daily_data.data)
            print(type(form.milked_date.data))
            for each_cust in form.daily_data:
                print (each_cust.loan.data,each_cust.loan_amount.data,"each cust",each_cust.loan)
                milk_data = Milk(
                    owner_id=each_cust.owner_id.data,
                    # After version 2.0
                    milker=each_cust.milker.data if not no_milker else 1,
                    milked_date=form.milked_date.data,
                    milked_time=form.milked_time.data,
                    litre=each_cust.litre.data,
                    ml=each_cust.ml.data,
                    price=form.price.data,
                    fodder=each_cust.fodder.data,
                    loan=each_cust.loan.data,
                    advance=each_cust.advance.data,
                    dr_service=each_cust.dr_service.data,
                    #loan_id=each_cust.loan_id.data,
                    #loan_payment=each_cust.loan_amount.data
                )
                db.session.add(milk_data)
            print("committing")
            db.session.commit()
            print("committed")
            return redirect(
                url_for('milk.add_daily_data', modified_day=form.milked_date.data, milked_time=form.milked_time.data))
        else:
            print("Hello", form.data)
            for each in form.daily_data:
                for m in milk_data:
                    # loan_data = LoanLedger.query.filter(LoanLedger.loan_id == each.loan_id.data).all()
                    print(each.loan_id.data,each.loan_amount.data, "each",each.loan)
                    # print ('N',n.milker_id,n.owner_id,n.milked_time,n.litre,n.ml,n.milked_date)
                    if m.owner_id == each.owner_id.data:
                        print("rim", form.milked_time.data)
                        # After version 2.0
                        m.milker_id = each.milker.data if not no_milker else 1
                        m.price = form.price.data
                        if form.milked_time.data == "am":
                            m.am_litre = Milk.litre_conv(m, each.litre.data, each.ml.data)
                        else:
                            m.pm_litre = Milk.litre_conv(m, each.litre.data, each.ml.data)
                        print("m", each.ml.data)
                        print("m", m.am_litre)
                        print(each.fodder.data, each.loan.data, each.advance.data)
                        m.fodder = each.fodder.data
                        m.loan = each.loan.data
                        m.advance = each.advance.data
                        m.dr_service = each.dr_service.data
                        if each.loan_amount.data:
                            remaining = LoanLedger.remaining(each.loan_id.data)
                            if remaining is None:
                                print ("No remaining Loan found")
                                remaining = Loan.loan_data(each.loan_id.data).loan_amount;
                            print (type(remaining),remaining, "reaming")
                            print(each.loan_amount.data, "payment done for ", each.loan_id.data)
                            loan_data=LoanLedger(
                                loan_id=each.loan_id.data,
                                loan_payment=each.loan_amount.data,
                                loan_payment_time=form.milked_date.data,
                                loan_remaining=remaining-each.loan_amount.data
                                                 )
                            db.session.add(loan_data)
                        db.session.add(m)
                    db.session.commit()
            print(form.milked_date.data)
            return redirect(url_for('milk.add_daily_data',
                                    modified_day=form.milked_date.data,
                                    milked_time=form.milked_time.data))

    for error, message in form.errors.items():
        print([(f.loan_id.data,f.loan_amount.data) for f in form.daily_data],"Form")
        print ([f.loan_id.data for f in form.daily_data])
        flash (form.daily_data)
        for m in message:
            flash(f"{error.capitalize()} : {m}", category='error')

    daily_data_form = DailyData()
    milk_header = [daily_data_form.owner_id.label,
                   daily_data_form.place.label,
                   daily_data_form.cust_name.label,
                   daily_data_form.litre.label,
                   daily_data_form.ml.label,
                   ]
    header = milk_header
    tm_header = ['வா.எண்', 'ஊர்', 'பெயர்', 'லிட்டர்', 'மில்லி']
    print("days", modified_day, day, milk_data_for_today, milked_time)
    for n in milk_data_for_today:
        print(n.milker_id, n.owner_id, n.am_litre, n.pm_litre)

    milking_charge = config_data()['milking_charge']

    return render_template('milk/daily_data.html',
                           form=form,
                           day=day,
                           no_milker=no_milker,
                           modified_day=modified_day,
                           milking_charge=milking_charge,
                           header=header,
                           tm_header=tm_header,
                           rate=rate,
                           milk_data_for_today=milk_data_for_today,
                           milked_time=milked_time,
                           customer_set=customers,
                           loan_details=loan_details,
                           owners_with_load=owners_with_load,
                           flash=flash)


@milk.route('/ledger/<month>', methods=["GET", "POST"])
@login_required
def milk_ledger_view(month=None):
    form = LedgerView()

    if month == "None":
        month = today_date.replace(day=1)
        print("Here is te month", month)
        return redirect(url_for('milk.milk_ledger_view', month=month))
    else:
        month = datetime.strptime(month, '%Y-%m-%d').date()

    ledger_obj = WholeMonthData(month)
    monthly_ledger = ledger_obj.ledger_calc()
    first = ledger_obj.first_day_of_month
    last = ledger_obj.last_day_of_month

    print("mon", type(month))
    print("data", monthly_ledger)
    # sheet_url = google_backup.spreadsheet_check(month.strftime("%Y")+"Paalkanakku").url
    sheet_url = "dumm"
    if check_google_sheet():
        sheet_url = check_google_sheet()
    else:
        sheet_url = google_backup.spreadsheet_check(month.strftime("%Y") + "Paalkanakku").url
        yaml_data = {'gsheet_url': sheet_url}
        print("Sheet Not found")
        with open(sheet_config, "a+") as w:
            data = yaml.dump(yaml_data, w)

    if form.validate_on_submit():
        print(form.month.data)
        monthly_ledger = ledger_obj.ledger_calc()
        print("mon", form.month.data)
        print("data", monthly_ledger)
        mon = google_backup.add_data_to_google(date_object=month, first=first, last=last)
        flash(f"The data is backed up for {mon}")
        return redirect(url_for("milk.milk_ledger_view", month=form.month.data))

    header = ['Place', 'Name', 'Milk', 'M.Charge', 'Fodder', 'Loan', 'Advance', 'Dr_service', 'Debit']
    tm_header = ['ஊர்', 'பெயர்', 'பால்', 'க.காசு', 'புண்ணாக்கு', 'கடன்', 'முன்பணம்', 'மருத்துவச் செலவு', 'பற்று ']

    return render_template('milk/view_ledger.html',
                           form=form,
                           month=month,
                           milking_charge=milking_charge,
                           tm_header=tm_header,
                           header=header,
                           monthly_ledger=monthly_ledger,
                           customer_set=customer_set(),
                           sheet_url=sheet_url)


# @crontab.job(minute="1", hour="*", day="*", month="*", day_of_week="*")
# def my_scheduled_job():
#     last_day_of_month = WholeMonthData(today_date).last_day_of_month
#     print("last", last_day_of_month, datetime.combine(today_date, datetime.min.time()))
#     if today_date == last_day_of_month:
#         print("Hello there")
#     prev_month_due = [(ledger[0], ledger[3] + ledger[4]
#                        - ledger[5]
#                        - ledger[6]
#                        - ledger[7]
#                        - ledger[8] - milking_charge) for ledger in WholeMonthData(today_date).ledger_calc()]
#     print(prev_month_due)

@milk.route('/invoice', methods=["GET", "POST"])
@login_required
def invoice_view():
    month = today_date.replace(day=1)

    ledger_obj = WholeMonthData(month)
    first = ledger_obj.first_day_of_month
    last = ledger_obj.last_day_of_month

    user_bill = google_backup.MilkData(first, last)
    per_user_bill = {}
    customer = customer_set()
    for c in customer:
        milk_data = user_bill.milk_data_customer_wise(c.owner_id)
        print(c.owner_id)
        print(milk_data)
        am = sum(data.am_litre for data in milk_data)
        pm = sum(data.pm_litre for data in milk_data)
        pm = sum(data.pm_litre for data in milk_data)
        fodder = sum(data.fodder for data in milk_data)
        loan = sum(data.loan for data in milk_data)
        advance = sum(filter(None, [data.advance for data in milk_data]))
        dr_service = sum(filter(None, [data.dr_service for data in milk_data]))
        total = sum(filter(None, [(data.am_litre + data.pm_litre) * data.price for data in milk_data]))

        per_user_bill[c.owner_id] = {'milk_data': milk_data,
                                     'am': am,
                                     'pm': pm,
                                     'fodder': fodder,
                                     'loan': loan,
                                     'advance': advance,
                                     'dr_service': dr_service,
                                     'total': total}

    header = ['Date', 'Morn', 'Evng', 'Fodder', 'Loan', 'Advance', 'Dr_service', 'Debit']
    tm_header = ['தேதி', 'காலை', 'மாலை', 'புண்ணாக்கு', 'கடன்', 'முன்பணம்', 'மருத்துவச் செலவு', 'பற்று ']

    return render_template('milk/invoice.html',
                           per_user_bill=per_user_bill,
                           header=header,
                           milking_charge=milking_charge,
                           tm_header=tm_header,
                           customer_set=customer)


@milk.route('/loan_ledger/<loan_id>', methods=["GET", "POST"])
@login_required
def loan_ledger(loan_id=None):
    form = LoanLedgerForm()
    loan_ledger_data = LoanLedger.query.filter(LoanLedger.loan_id == loan_id).all()
    loan_data = Loan.loan_data(loan_id)

    if not loan_ledger_data:
        loan_ledger_data = None
    owner_details = CowOwner.query.filter(CowOwner.owner_id == loan_data.owner_id).first()

    print(form.data, "fro be")
    if form.validate_on_submit():
        print (form.data,"froo")
        if form.delete.data:
            loan = LoanLedger.query.filter(LoanLedger.loan_payment_id == form.payment_id.data).delete()
            try:
                db.session.commit()
            except:
                flash(f"Some error in deleting the loan payment.")
            else:
                print (loan,"Loan id deleted")
                LoanLedger.query.filter(LoanLedger.loan_payment_id > form.payment_id.data).\
                    update({'loan_remaining': LoanLedger.loan_remaining+form.credit.data})
                db.session.commit()
                return redirect(url_for('milk.loan_ledger',loan_id=loan_id))
    print ("loan_data",loan_data)
    header = ["Loan Id", "Payment Date", "Credit", "Remaining"]
    tm_header = ['லோன் எண்', 'கட்டணத் தேதி', 'வரவு ', 'மீதம் ']
    return render_template('loan/loan_ledger.html',
                           loan_id=loan_id,
                           owner_details=owner_details,
                           header=header,
                           loan_data=loan_data,
                           tm_header=tm_header,
                           loan_ledger_data=loan_ledger_data,
                           form=form,
                           flash=flash)

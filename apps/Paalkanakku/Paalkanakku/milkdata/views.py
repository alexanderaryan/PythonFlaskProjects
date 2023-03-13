from datetime import datetime, timedelta


#####################weasyprint
from weasyprint import HTML
import io

###################pdf
from flask import send_file,Response
from fpdf import FPDF

from borb.pdf.document import document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image

from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
from datetime import datetime
import random
from borb.pdf.pdf import PDF
from borb.pdf.canvas.color.color import HexColor, X11Color

from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.table.table import TableCell

##################pdf


from sqlalchemy import func
import yaml

try:
    from Paalkanakku import app, db, today_date, crontab
    from Paalkanakku.models import Milkers, CowOwner, Milk, Loan, LoanLedger, MilkCharge
    from Paalkanakku.milkdata.forms import AddDailyData, DailyData, LedgerView, milker_data, loan_choice
    from Paalkanakku.owner.forms import LoanLedgerForm
    from Paalkanakku.milkdata import google_backup
    from Paalkanakku.config import sheet_config
except:
    from Paalkanakku.Paalkanakku import app, db, today_date, crontab
    from Paalkanakku.Paalkanakku.models import Milkers, CowOwner, Milk, Loan, LoanLedger, MilkCharge
    from Paalkanakku.Paalkanakku.owner.forms import LoanLedgerForm
    from Paalkanakku.Paalkanakku.milkdata.forms import AddDailyData, DailyData, LedgerView, milker_data, loan_choice
    from Paalkanakku.Paalkanakku.milkdata import google_backup
    from Paalkanakku.Paalkanakku.config import sheet_config

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

milk = Blueprint('milk', __name__)


def check_google_sheet(year=datetime.today().year):
    with open(sheet_config) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data, "total file", year)
        try:
            sheet_url = data['gsheets_url'][year]
            print ("inside",sheet_url,year)
            return sheet_url
        except KeyError:
            print(f"KeyError, Year {year} sheet is yet to be created")
            return False
        # else:
        #     sheet_url = data['gsheets_url'][year]
        #     return sheet_url
        #
        #
        # if data['gsheets_url'][int(year)] is not None:
        #     print(data['gsheets_url'])
        #     sheet_url = data['gsheets_url']
        #     return sheet_url
        # else:
        #     return False


def config_data():
    stream = open(sheet_config, 'r')
    data = yaml.load(stream, Loader=yaml.FullLoader)

    return data


milking_charge = config_data()['milking_charge']


def milk_charge_check(month,year):

    milk_charge = MilkCharge.query.filter(MilkCharge.milk_charge_month == month).\
        filter(MilkCharge.milk_charge_year == year).first()
    if not milk_charge:
        print("milkcharge is not in table")
    else:
        print("milkcharge is in the table")

    return milk_charge if milk_charge else False




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

    print (milk_data)
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

        self.loan_data_query = LoanLedger.query.with_entities(Loan.owner_id,
                                                   func.coalesce(func.sum(LoanLedger.loan_payment), 0.0).
                                                   label('Loan_Total')). \
            join(Loan). \
            filter(LoanLedger.loan_payment_time.between(self.first_day_of_month, self.last_day_of_month))

    def ledger_calc(self, owner_id=None):
        """To return monthly legderdata"""

        print(self.milk_data_query.group_by(Milk.owner_id).order_by(Milk.owner_id))
        if owner_id:
            milk_data = self.milk_data_query.filter(Milk.owner_id == owner_id).group_by(Milk.owner_id).\
                order_by(Milk.owner_id).all()
            loan_data = self.loan_data_query.filter(LoanLedger.owner_id == owner_id).group_by(Loan.owner_id).\
                order_by(LoanLedger.owner_id).all()
        else:
            milk_data = self.milk_data_query.group_by(Milk.owner_id).order_by(Milk.owner_id).all()
            loan_data = self.loan_data_query.group_by(Loan.owner_id).order_by(LoanLedger.owner_id).all()
        print(loan_data, "Loan data n")
        print(self.first_day_of_month, self.last_day_of_month)
        if milk_data and loan_data:
            whole_data=[]
            common_elements = set([x[0] for x in milk_data]).intersection(set([y[0] for y in loan_data]))
            milk_data_new = list(map(list,milk_data))
            loan_data_new = list(map(list,loan_data))
            for m in milk_data_new:
                for l in loan_data_new:
                    if m[0] == l[0] and m[0] in common_elements and l[0] in common_elements:
                        m.append(l[1])
                        whole_data.append(m)
                    elif m[0] not in common_elements:
                        m.append(0)
                        whole_data.append(m)
                        break
            print (whole_data, "whole data")
            milk_data = whole_data

        print("whole", milk_data)
        return milk_data


"""def milker_set():
    

    milker_data = Milkers.query.all()
    milker_ids = [milker.milker_id for milker in milker_data]
    milkers = [(milker.milker_id, milker.name) for milker in milker_data]

    return milkers,milker_ids"""


def customer_set(active=False,owner=None):
    """
    To give the set of customers added in the Owners Table
    """
    milker_ids = milker_data()[1]
    print (milker_ids,"inside customer set", active)
    try:
        if not active:
            if owner:
                customer = (CowOwner.query. \
                        filter(CowOwner.milker_id.in_(milker_ids)).filter(CowOwner.owner_id==owner).group_by(CowOwner.owner_id). \
                        order_by(CowOwner.place, CowOwner.name).all())
            else:
                customer = (CowOwner.query. \
                            filter(CowOwner.milker_id.in_(milker_ids)).group_by(CowOwner.owner_id). \
                            order_by(CowOwner.place, CowOwner.name).all())
        else:

            customer = (CowOwner.query. \
                        filter(CowOwner.milker_id.in_(milker_ids),CowOwner.active == True).group_by(CowOwner.owner_id). \
                        order_by(CowOwner.place, CowOwner.name).all())  #Do not change == for cowowner.active
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

    owners_with_loan = Loan.owners_with_loan()
    print(owners_with_loan)
    for n in milk_data_for_today:
        print("milker", n.milker_id, n.am_litre, n.pm_litre)
    if not milk_data_for_today:
        print ("inn")
        if not no_milker:
            form.daily_data[0].milker.choices = milker_data(False)[2]
            print(milker_data(False)[2],"h")
        print ("out")
        customers = customer_set(True)
    else:
        if not no_milker:
            form.daily_data[0].milker.choices = milker_data()[2]
            print(milker_data(False)[2],"g")
        customers = customer_set()

    # print("Length", len(customers), len(milk_data_for_today))
    print("customers", customers)
    print(form.data, "data of form")
    print("Form validation is ", form.validate_on_submit())

    if form.validate_on_submit():
        print ("Where")
        print([(f.loan_id.data, f.loan_amount.data) for f in form.daily_data], "Form")
        if form.milking_charge.data:

            milk_charge = milk_charge_check(form.milked_date.data.month,
                                     form.milked_date.data.year)
            if milk_charge:
                print (f"Milk charge is there for {form.milked_date.data.month} {form.milked_date.data.year}")
                milk_charge.milk_charge = form.milking_charge.data
                db.session.add(milk_charge)
                try:
                    db.session.commit()
                except:
                    print (f"Error in updating milk_charge for {form.milked_date.data.month} {form.milked_date.data.year}")
                else:
                    print (f"Milk charge successfully updated for {form.milked_date.data.month}"
                           f" {form.milked_date.data.year}")
            else:
                milk_charge = MilkCharge(form.milking_charge.data, form.milked_date.data.month,
                                     form.milked_date.data.year)
                db.session.add(milk_charge)
                try:
                    db.session.commit()
                except:
                    print(
                        f"Error in Adding milk_charge for {form.milked_date.data.month} {form.milked_date.data.year}")
                else:
                    print(f"Milk charge successfully updated for {form.milked_date.data.month}"
                          f" {form.milked_date.data.year}")
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
                if each_cust.loan_amount.data:
                    print(each_cust.loan_amount.data,"loan data")
                    remaining = LoanLedger.remaining(each_cust.loan_id.data)
                    if remaining is None:
                        print("No remaining Loan found")
                        remaining = Loan.loan_data(each_cust.loan_id.data).loan_amount;
                    print(type(remaining), remaining, "reaming")
                    print(each_cust.loan_amount.data, "payment done for ", each_cust.loan_id.data)
                    print (each_cust.loan_amount.data < remaining)
                    if each_cust.loan_amount.data < remaining:
                        loan_data = LoanLedger(
                            loan_id=each_cust.loan_id.data,
                            loan_payment=each_cust.loan_amount.data,
                            loan_payment_time=form.milked_date.data,
                            loan_remaining=remaining - each_cust.loan_amount.data,
                            owner_id=each_cust.owner_id.data
                        )
                        db.session.add(loan_data)
                        db.session.commit()
                    else:
                        flash(f"Loan Payment for Loan ID exceeds remaining : {remaining}", category='error')
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
                            print (each.loan_amount.data < remaining,"ejere")
                            if each.loan_amount.data < remaining:
                                loan_data=LoanLedger(
                                    loan_id=each.loan_id.data,
                                    owner_id=each.owner_id.data,
                                    loan_payment=each.loan_amount.data,
                                    loan_payment_time=form.milked_date.data,
                                    loan_remaining=remaining-each.loan_amount.data
                                                     )
                                db.session.add(loan_data)
                                db.session.commit()
                            else:
                                flash(f"Loan Payment for Loan ID exceeds remaining : {remaining}", category='error')
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

    milked_charge = milk_charge_check(day.month,day.year).milk_charge if milk_charge_check(day.month,day.year) else 0

    return render_template('milk/daily_data.html',
                           form=form,
                           day=day,
                           no_milker=no_milker,
                           modified_day=modified_day,
                           milking_charge=milked_charge,
                           header=header,
                           tm_header=tm_header,
                           rate=rate,
                           milk_data_for_today=milk_data_for_today,
                           milked_time=milked_time,
                           customer_set=customers,
                           loan_details=loan_details,
                           owners_with_loan=owners_with_loan,
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
    year = month.year
    sheet_url = check_google_sheet(year=year)
    print(year , "monthd")
    if not sheet_url:
        print("No Sheet")
        sheet_url = google_backup.spreadsheet_check(f"{year}Paalkanakku").url
        yaml_data = {'gsheet_url': sheet_url}
        yaml_data = {'gsheet_url': {year: sheet_url}}
        with open(sheet_config) as f:
            sheet_data = yaml.load(f, Loader=yaml.FullLoader)
        print("Sheet Not found,here")
        sheet_data['gsheets_url'][year] = sheet_url
        with open(sheet_config, 'w') as f:
            yaml.dump(sheet_data, f)

        # with open(sheet_config, "a+") as w:
        #     data = yaml.dump(yaml_data, w)

    for error, message in form.errors.items():
        print([(f.loan_id.data,f.loan_amount.data) for f in form.daily_data],"Form")
        print([f.loan_id.data for f in form.daily_data])
        flash(form.daily_data)
        for m in message:
            flash(f"{error.capitalize()} : {m}", category='error')
    print(form.data,"errors")
    if form.validate_on_submit():
        print(form.month.data)
        monthly_ledger = ledger_obj.ledger_calc()
        print("mon", form.month.data)
        print("data", monthly_ledger)
        mon = google_backup.add_data_to_google(date_object=month, first=first, last=last)
        flash(f"The data is backed up for {mon}")
        return redirect(url_for("milk.milk_ledger_view", month=form.month.data))

    header = ['Na   me','Place', 'Milk', 'M.Charge', 'Fodder', 'Loan', 'Advance', 'Dr_service', 'Debit']
    tm_header = ['பெயர்', 'ஊர்','பால்', 'க.காசு', 'புண்ணாக்கு', 'கடன்', 'முன்பணம்', 'மருத்துவச் செலவு', 'பற்று ']

    milked_charge = milk_charge_check(month.month, year).milk_charge if milk_charge_check(month.month, year) else 0
    print (f"{month} {year} {milked_charge}","oioii")

    return render_template('milk/view_ledger.html',
                           form=form,
                           month=month,
                           milking_charge=milked_charge,
                           tm_header=tm_header,
                           header=header,
                           monthly_ledger=monthly_ledger,
                           customer_set=customer_set(),
                           sheet_url=sheet_url,
                           flash=flash)


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

# @milk.route('/invoice', methods=["GET", "POST"])
# @login_required
# def invoice_view():
#
#     month = today_date.replace(day=1)
#     ledger_obj = WholeMonthData(month)
#     first = ledger_obj.first_day_of_month
#     last = ledger_obj.last_day_of_month
#
#     user_bill = google_backup.MilkData(first, last)
#     per_user_bill = {}
#     customer = customer_set()
#     for c in customer:
#         milk_data,kk_data = user_bill.milk_data_customer_wise(c.owner_id)
#         ledger_obj = WholeMonthData(month)
#         monthly_ledger = ledger_obj.ledger_calc(c.owner_id)
#         am = sum(data.am_litre for data in milk_data)
#         pm = sum(data.pm_litre for data in milk_data)
#         fodder = sum(data.fodder for data in milk_data)
#         try:
#             loan = monthly_ledger[0][9]
#         except IndexError:
#             loan = 0
#         advance = sum(filter(None, [data.advance for data in milk_data]))
#         dr_service = sum(filter(None, [data.dr_service for data in milk_data]))
#         total = sum(filter(None, [(data.am_litre + data.pm_litre) * data.price for data in milk_data]))
#
#         per_user_bill[c.owner_id] = {'milk_data': milk_data,
#                                      'am': am,
#                                      'pm': pm,
#                                      'fodder': fodder,
#                                      'loan': loan,
#                                      'advance': advance,
#                                      'dr_service': dr_service,
#                                      'total': total}
#
#     header = ['Date', 'Morn', 'Evng', 'Fodder', 'Loan', 'Advance', 'Dr_service', 'Debit']
#     tm_header = ['தேதி', 'காலை', 'மாலை', 'புண்ணாக்கு', 'கடன்', 'முன்பணம்', 'மருத்துவச் செலவு', 'பற்று ']
#
#     return render_template('milk/invoice.html',
#                            per_user_bill=per_user_bill,
#                            header=header,
#                            milking_charge=milking_charge,
#                            tm_header=tm_header,
#                            customer_set=customer)


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
            LoanLedger.query.filter(LoanLedger.loan_payment_id == form.payment_id.data).delete()
            try:
                db.session.commit()
            except:
                flash(f"Some error in deleting the loan payment.")
            else:
                LoanLedger.query.filter(LoanLedger.loan_payment_id > form.payment_id.data).\
                    update({'loan_remaining': LoanLedger.loan_remaining+form.credit.data})
                db.session.commit()
                flash(f"Loan payment id deleted successfully")
                return redirect(url_for('milk.loan_ledger',loan_id=loan_id))

        elif form.submit.data:
            loan_item = LoanLedger.query.filter(LoanLedger.loan_payment_id == form.payment_id.data).first()
            if loan_item.loan_payment_id == form.payment_id.data:
                print (loan_item.loan_payment < form.credit.data,"cond",loan_item.loan_payment,form.credit.data)
                if loan_item.loan_payment < form.credit.data:
                    additional_amount = form.credit.data - loan_item.loan_payment
                    loan_item.loan_remaining -= additional_amount
                    LoanLedger.query.filter(LoanLedger.loan_payment_id > form.payment_id.data). \
                        update(
                        {'loan_remaining': LoanLedger.loan_remaining - additional_amount})
                else:
                    extra_amount = loan_item.loan_payment - form.credit.data
                    print (extra_amount,"extra")
                    loan_item.loan_remaining += extra_amount
                    LoanLedger.query.filter(LoanLedger.loan_payment_id > form.payment_id.data). \
                        update(
                        {'loan_remaining': LoanLedger.loan_remaining + extra_amount})
                loan_item.loan_payment = form.credit.data
                loan_item.loan_payment_time = form.loan_payment_date.data
                db.session.add(loan_item)

            #     update({'loan_payment': form.credit.data,
            #             'loan_payment_time': form.loan_payment_date.data,
            #             'loan_remaining': LoanLedger.loan_remaining + form.credit.data - LoanLedger.loan_payment})
            # LoanLedger.query.filter(LoanLedger.loan_payment_id > form.payment_id.data). \
            #     update({'loan_remaining': LoanLedger.loan_remaining + form.credit.data})
            try:
                db.session.commit()
            except:
                flash(f"Some error in updating the loan payment.")
            else:
                flash(f"Loan payment id updated successfully")

    print ("loan_data",loan_data)
    header = ["Loan Id", "Payment Date", "Credit", "Remaining",""]
    tm_header = ['லோன் எண்', 'கட்டணத் தேதி', 'வரவு ', 'மீதம்',""]
    return render_template('loan/loan_ledger.html',
                           loan_id=loan_id,
                           owner_details=owner_details,
                           header=header,
                           loan_data=loan_data,
                           tm_header=tm_header,
                           loan_ledger_data=loan_ledger_data,
                           form=form,
                           flash=flash)

#
# @milk.route('/invoice_ledger_pfdf', methods=["GET", "POST"])
# @login_required
# def invoice_loan_ledger(loan_id=None):
#
#     """
#     This function will generate pdf of invoices to all the customers
#     """
#     pdf = FPDF()
#     pdf.add_page()
#
#     page_width = pdf.w - 2 * pdf.l_margin
#
#     pdf.set_font('Times', 'B', 14.0)
#     pdf.cell(page_width, 0.0, 'Employee Data', align='C')
#     pdf.ln(10)
#
#     pdf.set_font('Courier', '', 12)
#
#     col_width = page_width / 4
#
#     pdf.ln(1)
#
#     th = pdf.font_size
#
#     result = [{'emp_id':1,'emp_first_name':"Alex","emp_last_name":"M","emp_designation":"IT"},
#               {'emp_id':2,'emp_first_name':"Alex","emp_last_name":"M","emp_designation":"IT"},
#               {'emp_id':3,'emp_first_name':"Alex","emp_last_name":"M","emp_designation":"IT"},]
#     for row in result:
#         pdf.cell(col_width, th, str(row['emp_id']), border=1)
#         pdf.cell(col_width, th, row['emp_first_name'], border=1)
#         pdf.cell(col_width, th, row['emp_last_name'], border=1)
#         pdf.cell(col_width, th, row['emp_designation'], border=1)
#         pdf.ln(th)
#
#     pdf.ln(10)
#
#     pdf.set_font('Times', '', 10.0)
#     pdf.cell(page_width, 0.0, '- end of report -', align='C')
#
#
#     return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
#                     headers={'Content-Disposition': 'attachment;filename=employee_report.pdf'})
#


@milk.route('/invoice_ledger/<month>', methods=["GET", "POST"])
@login_required
def invoice_loan_led(month=None, customer=None):

    """
    This function will generate pdf of invoices to all the customers
    """

    customer = request.args.get('customer', None)
    print (month,customer)
    html = HTML('Paalkanakku/templates/milk/invoice_weasy.html')

    today = datetime.today().strftime("%B %-d, %Y")
    invoice_number = 123
    from_addr = {
        'company_name': 'Company Name',
        'addr1': '455 A. Vallalapatti,',
        'addr2': 'Melur, Madurai 625301'
    }
    to_addr = {
        'company_name': 'Acme Corp',
        'person_name': 'John Dilly',
        'person_email': 'john@example.com'
    }
    items = [
        {
            'title': 'website design',
            'charge': 300.00
        }, {
            'title': 'Hosting (3 months)',
            'charge': 75.00
        }, {
            'title': 'Domain name (1 year)',
            'charge': 10.00
        }
    ]
    duedate = "August 1, 2018"
    total = sum([i['charge'] for i in items])

    #######################################

    if month == "None":
        month = today_date.replace(day=1)
    else:
        month = datetime.strptime(month, '%Y-%m-%d').date()

    ledger_obj = WholeMonthData(month)
    first = ledger_obj.first_day_of_month
    last = ledger_obj.last_day_of_month

    user_bill = google_backup.MilkData(first, last)
    per_user_bill = {}
    if not customer:
        print("dfdsfdf", customer)
        customer = customer_set()
    else:
        print("ooioidoisd",customer)
        customer = customer_set(owner=customer)
        print("ooioidoisd")
    for c in customer:
        milk_data, kk_data = user_bill.milk_data_customer_wise(c.owner_id)
        ledger_obj = WholeMonthData(month)
        monthly_ledger = ledger_obj.ledger_calc(c.owner_id)
        am = sum(data.am_litre for data in milk_data)
        pm = sum(data.pm_litre for data in milk_data)
        fodder = sum(data.fodder for data in milk_data)
        try:
            loan = monthly_ledger[0][9]
        except IndexError:
            loan = 0
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


    ################################
    milked_charge = milk_charge_check(month.month, month.year).milk_charge if milk_charge_check(month.month, month.year) else 0

    return render_template('milk/invoice_weasy.html',
                               date=today,
                               from_addr=from_addr,
                               to_addr=to_addr,
                               items=items,
                               total=total,
                               invoice_number=invoice_number,
                               duedate=duedate,
                               per_user_bill=per_user_bill,
                               header=header,
                               milking_charge=milked_charge,
                               tm_header=tm_header,
                               customer_set=customer
                               )
    html = HTML(string=rendered)
    rendered_pdf = html.write_pdf()
    # rendered_pdf = html.write_pdf('invoice.pdf')
    return send_file(
        io.BytesIO(rendered_pdf),
            attachment_filename='invoice.pdf'
        )
    #If we need to change the button as downloading
    # return send_file("../invoice.pdf",attachment_filename="out.pdf",date=today)

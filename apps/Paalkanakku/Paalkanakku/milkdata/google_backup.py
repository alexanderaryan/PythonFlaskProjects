
import gspread
from datetime import datetime
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import text


try:

    from Paalkanakku.models import Milk,LoanLedger
    from Paalkanakku import db

except:

    from Paalkanakku.Paalkanakku.models import Milk,LoanLedger
    from Paalkanakku.Paalkanakku import db

gc = gspread.service_account()


def to_del_all_spreadsheets(gc):

    """Use this if you wish to delete all worksheets"""

    xx = gc.list_spreadsheet_files()
    for x in xx:
        print (x['id'])
        gc.del_spreadsheet(x['id'])


def spreadsheet_check(sheet_name):
    try:
        sh = gc.open(sheet_name)
    except Exception as e:
        er = e.__class__.__name__
        if er == 'SpreadsheetNotFound':
            print (f"Sheet {sheet_name} Not found!")
            sh = gc.create(sheet_name)
            sheet_id = sh.id
            print(f"Sheet {sheet_name} created")
            sh.share('alextechie2020@gmail.com', perm_type='user', role='reader')
            print(current_user.email)
            sh.share(current_user.email, perm_type='user', role='reader')
            return sh
    else:
        sheet_id = sh.id

    return sh


def worksheet_check(sh,month):
    # sheet_list = gc.list_spreadsheet_files(sheet_name)
    # for n in sheet_list:
    #     print (n)
    sheets = sh.worksheets()
    sheet_names = [sheet.title for sheet in sheets]
    if month not in sheet_names:
        print (f"Sheet {month} not in {sh.title}")
        worksheet_id = sh.add_worksheet(month,100,100).id
        worksheet = sh.get_worksheet_by_id(worksheet_id)
    else:
        print(f"Sheet {month} is in {sh.title}")
        index = sheet_names.index(month)
        worksheet = sh.get_worksheet(index)
    print (worksheet)
    return worksheet


class MilkData:

    def __init__(self,first,last):
        self.first = first
        self.last = last
        self.milk_data_query = Milk.query.filter(Milk.milked_date.between(first, last))

    def milk_data_date_wise(self):

        milk_data = self.milk_data_query.\
            order_by(Milk.milked_date).all()

        # milk_data = list(map(list, milk_data))
        # for ind, n in enumerate(milk_data):
        #     kl = datetime.strftime(n[3], '%Y-%m-%d')
        #     milk_data[ind][3] = kl

        return milk_data

    def milk_data_customer_wise(self,owner_id):

        milk_data = self.milk_data_query.\
            join(LoanLedger,Milk.owner_id == LoanLedger.owner_id).\
            order_by( Milk.owner_id, Milk.milked_date).\
            filter(Milk.owner_id == owner_id). \
            all()
        #
        # kk_data = db.session.query(Milk.owner_id,
        #                            Milk.price,
        #                            func.coalesce(func.sum(func.distinct(Milk.am_litre)), 0.0).label('AM_Total'),
        #                            func.coalesce(func.sum(func.distinct(Milk.pm_litre)), 0.0).label('PM_Total'),
        #                            func.coalesce(func.sum(func.distinct(Milk.am_litre) * Milk.price), 0.0).label(
        #                                'AM_Total_Price'),
        #                            func.coalesce(func.sum(func.distinct(Milk.pm_litre) * Milk.price), 0.0).label(
        #                                'PM_Total_Price'),
        #                            func.coalesce(func.sum(func.distinct(Milk.fodder)), 0.0).label('Fodder'),
        #                            func.coalesce(func.sum(func.distinct(Milk.advance)), 0.0).label('Advance'),
        #                            func.coalesce(func.sum(func.distinct(Milk.dr_service)), 0.0).label(
        #                                'Dr_service'),
        #                            func.coalesce((func.distinct(LoanLedger.loan_payment)), 0.0).label('Loan'),
        #                            ).outerjoin(LoanLedger,Milk.owner_id == LoanLedger.owner_id).\
        #     filter(Milk.owner_id == owner_id).distinct(). \
        #     group_by(Milk.owner_id).\
        #     all()
        kk_data_cmd = """ select distinct * from loanledger join milk on milk.owner_id = loanledger.owner_id 
        where milk.owner_id=1001 group by milk.event_id;"""
        kk_data = db.session.execute(
            text(kk_data_cmd),
            {"db": "classicmodels"}
        )
        kk_data=kk_data.fetchall()
        # print(kk_data, "kk data",len(kk_data))
        kk_data = set(kk_data)
        # print (kk_data,"kk data",len(set(kk_data)))
        # milk_data = list(map(list, milk_data))
        # for ind, n in enumerate(milk_data):
        #     kl = datetime.strftime(n[3], '%Y-%m-%d')
        #     milk_data[ind][3] = kl

        return milk_data,kk_data


def add_data_to_google(date_object, first, last):

    year = date_object.strftime("%Y")+"Paalkanakku"
    month = date_object.strftime("%b %Y")
    print ("year", year)
    print("month", month)
    sh = spreadsheet_check(year)
    worksheet = worksheet_check(sh, month)
    #milk_data = WholeMonthData(month)
    worksheet.clear()
    print (f"worksheet_cleared")
    worksheet.append_row(Milk.__table__.columns.keys())
    worksheet.freeze(rows=1)
    # Set 'A4' cell's text format to bold
    # worksheet.format("A4", {"textFormat": {"bold": True}})
    #
    # # Color the background of 'A2:B2' cell range in black,
    # # change horizontal alignment, text color and font size
    # worksheet.format("A1:G15", {
    #     "backgroundColor": {
    #         "red": 0.0,
    #         "green": 0.0,
    #         "blue": 0.0
    #     },
    #     "horizontalAlignment": "CENTER",
    #     "textFormat": {
    #         "foregroundColor": {
    #             "red": 1.0,
    #             "green": 1.0,
    #             "blue": 1.0
    #         },
    #         "fontSize": 12,
    #         "bold": True
    #     }
    # })
    print(f"Title added")
    milk_obj = MilkData(first,last)
    milk_data = milk_obj.milk_data_date_wise()
    print (milk_data)
    data = [[d.event_id,d.owner_id,
           d.milker_id,datetime.strftime(d.milked_date,"%d-%m-%Y"),
           d.am_litre,d.pm_litre,
           d.price,d.fodder,d.advance,
           d.loan,d.dr_service] for d in milk_data]
    print (data)
    worksheet.append_rows(data)
    return month
    # print("man eo",worksheet.range(1,1, worksheet.row_count, worksheet.col_count))
    #
    #
    # query = Milk.query.filter()
    # milk_data = query.with_entities(Milk.event_id, Milk.owner_id, Milk.milker_id, Milk.milked_date, Milk.am_litre,
    #                     Milk.pm_litre, Milk.price).all()
    # print(milk_data)
    # print(query._raw_columns)
    #
    # milk_data = list(map(list, milk_data))
    # for ind, n in enumerate(milk_data):
    #     kl = datetime.strftime(n[3], '%Y-%m-%d')
    #     print(kl)
    #     milk_data[ind][3] = kl
    #     print(milk_data)
    #
    # print (worksheet.row_count)
    #
    # worksheet = sh.get_worksheet(0)
    # print(worksheet.title)
    # worksheet.update_title("Feb 2022")
# worksheet = sh.worksheets()
# print (worksheet[0].title)
# print (WholeMonthData(datetime.date(datetime.today()).replace(day=1)))
#
# attributes = inspect.getmembers(Milk, lambda a:not(inspect.isroutine(a)))
# print ([a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))])
# print (Milk.__table__.columns.keys())
#
# print (dir(query))
# print (",".join(Milk.__table__.columns.keys()))

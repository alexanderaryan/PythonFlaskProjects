
import gspread
from datetime import datetime
from flask_login import current_user

try:

    from Paalkanakku.models import Milk
    from Paalkanakku import db

except:

    from Paalkanakku.Paalkanakku.models import Milk
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


def milk_data_query(first,last):

    milk_data = Milk.query.with_entities(Milk.event_id, Milk.owner_id, Milk.milker_id, Milk.milked_date,
                                         Milk.am_litre,
                                         Milk.pm_litre,
                                         Milk.price). \
        filter(Milk.milked_date.between(first, last)). \
        order_by(Milk.milked_date).all()

    milk_data = list(map(list, milk_data))
    for ind, n in enumerate(milk_data):
        kl = datetime.strftime(n[3], '%Y-%m-%d')
        print(kl)
        milk_data[ind][3] = kl

    return milk_data


def add_data_to_google(date_object, first, last):

    year = date_object.strftime("%Y")+"Paalkanakku"
    month = date_object.strftime("%b %Y")
    print ("year", year)
    print("month", month)
    sh = spreadsheet_check(year)
    worksheet = worksheet_check(sh, month)
    #milk_data = whole_month_data(month)
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
    milk_data = milk_data_query(first,last)
    print (milk_data)

    worksheet.append_rows(milk_data)
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
# print (whole_month_data(datetime.date(datetime.today()).replace(day=1)))
#
# attributes = inspect.getmembers(Milk, lambda a:not(inspect.isroutine(a)))
# print ([a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))])
# print (Milk.__table__.columns.keys())
#
# print (dir(query))
# print (",".join(Milk.__table__.columns.keys()))

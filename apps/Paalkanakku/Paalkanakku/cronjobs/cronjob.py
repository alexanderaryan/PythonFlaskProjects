from datetime import timedelta

try:
    from Paalkanakku import today_date, crontab, sched, db
    from Paalkanakku.models import Milkers, CowOwner, Milk
    from Paalkanakku.milkdata.views import WholeMonthData, price
    from Paalkanakku.milkdata.views import milking_charge
    from Paalkanakku.milkdata import google_backup
except:
    from Paalkanakku.Paalkanakku import app, db, today_date, crontab, sched
    from Paalkanakku.Paalkanakku.models import Milkers, CowOwner, Milk
    from Paalkanakku.Paalkanakku.milkdata.views import WholeMonthData, price
    from Paalkanakku.Paalkanakku.milkdata.views import milking_charge
    from Paalkanakku.Paalkanakku.milkdata import google_backup


def my_scheduled_job():

    ledger_obj = WholeMonthData(today_date.replace(day=1))
    last_day_of_month = ledger_obj.last_day_of_month
    if today_date == last_day_of_month:
        print("Hello there")
    prev_month_due = [(ledger[0], ledger[3] + ledger[4]
                       - ledger[5]
                       - ledger[6]
                       - ledger[7]
                       - ledger[8] - milking_charge) for ledger in ledger_obj.ledger_calc()]
    print(prev_month_due)

    milk_price = price(today_date)

    for owner,balance in prev_month_due:
        print (owner,balance, last_day_of_month + timedelta(days=1))
        milk_data = Milk.query.filter(Milk.owner_id == owner).filter(Milk.milked_date == last_day_of_month + timedelta(days=1))
        milk_data.delete()
        if not milk_data.all():
            milk_data = Milk(
                owner_id=owner,
                milker=1,
                milked_time='am',
                litre=0,
                ml=0,
                price=milk_price,
                milked_date=last_day_of_month + timedelta(days=1),
                advance=round(balance, 2) if balance<0 else 0,
            )
            db.session.add(milk_data)
            print (owner, balance, "added")
        else:
            print (f"Loan details are added already or the Owner {owner}")
        db.session.commit()


def google_backup_cron():

    month = today_date.replace(day=1)
    ledger_obj = WholeMonthData(month)
    last_day_of_month = ledger_obj.last_day_of_month
    mon = google_backup.add_data_to_google(date_object=month,
                                         first=ledger_obj.first_day_of_month,
                                         last=ledger_obj.last_day_of_month)


sched.add_job(my_scheduled_job,'cron',day='last')
sched.add_job(google_backup_cron,'cron',hour='23',minute='59')

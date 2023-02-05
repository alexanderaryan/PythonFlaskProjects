try:
    from Paalkanakku import app, db, today_date
    from Paalkanakku.models import Milkers, CowOwner, Milk, Loan
    from Paalkanakku.owner.forms import AddCustForm, DeleteCustForm, EditUserForm, AddLoanForm
    from Paalkanakku.users.views import add_profile_pic
    from Paalkanakku.milkdata.views import WholeMonthData

except:
    from Paalkanakku.Paalkanakku import app, db, today_date
    from Paalkanakku.Paalkanakku.models import Milkers, CowOwner, Milk, Loan
    from Paalkanakku.Paalkanakku.owner.forms import AddCustForm, DeleteCustForm, EditUserForm, AddLoanForm
    from Paalkanakku.Paalkanakku.users.views import add_profile_pic
    from Paalkanakku.Paalkanakku.milkdata.views import WholeMonthData

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

owner = Blueprint('owner', __name__)


def check_own_email(email, owner):
    "To chek if an email is taken already"
    print(email, "came in")
    if email:
        print(email, "email")
        if CowOwner.query.filter(CowOwner.email == email).filter(CowOwner.owner_id != owner).first():
            return True


def check_own_phone(phone, owner):
    "To chek if an email is taken already"
    if phone:
        if CowOwner.query.filter(CowOwner.phone_number == phone).filter(CowOwner.owner_id != owner).first():
            return True


def check_milker(name, place):
    """
    To return the details of the owners available already
    """
    owner_detail = CowOwner.query.filter_by(name=name, place=place).all()
    if owner_detail:
        return owner_detail


def milker_choice():
    milkers = Milkers.query.filter(Milkers.active == True).all()
    choices = [(str(o.milker_id), o.name) for o in milkers]
    return choices


@owner.route('/add_own', methods=['GET', 'POST'])
@login_required
def add_own():
    form = AddCustForm()

    # milkers = Milkers.query.filter(Milkers.active == True).all()
    # choices = [(str(o.milker_id), o.name) for o in milkers]
    # print(choices)
    form.milker_id.choices = milker_choice()

    print(form.data)
    if form.validate_on_submit():
        total_rows = CowOwner.query.count()
        name = form.name.data
        place = form.place.data
        owner_id = total_rows + 1000
        x = 0
        objects = []
        new_milkers = []
        for milker in form.milker_id.data:
            x += 1
            print(x, "x")
            owners_list = check_milker(name, place)
            milker = int(milker)
            print(owners_list, "printing out")
            print(milker, "milker check")

            if owners_list is None:
                new_milkers.append(milker)
                print(owners_list, "Inside")
                owner_data = CowOwner(
                    owner_id=owner_id,
                    name=name,
                    place=place,
                    num_cows=form.cows.data,
                    milker_id=milker
                )
                objects.append(owner_data)
                print(owner_data, "Hello there")
            else:
                milker_list = [owner.milker_id for owner in owners_list]
                owner_id = owners_list[0].owner_id
                print(owner_id)
                print(milker_list)
                if milker not in milker_list:
                    new_milkers.append(milker)
                    owner_data = CowOwner(
                        owner_id=owner_id,
                        name=name,
                        place=place,
                        num_cows=form.cows.data,
                        milker_id=int(milker)
                    )
                    # db.session.add(owner_data)
                    objects.append(owner_data)
                    print(owner_data, "after")
                    """try:
                        print("Trying to commit")
                        db.session.commit()
                    except:
                        print("Failed to commit")
                        db.session.rollback()
                        flash("Error in Adding New Owner!")
                    else:
                        flash(f"Owner {form.name.data} is Successfully Added with Milker {milker}!")"""
                else:
                    flash(f"Milker {milker} is already linked to {name}")

            print("Ended for")

        try:
            print(objects, "total obj")
            db.session.add_all(objects)
            print("Trying to commit")
            db.session.commit()
        except:
            print("Failed to commit")
            db.session.rollback()
            flash("Error in Adding New Owner!")
        else:
            flash(f"Owner {form.name.data} is Successfully Added with Milker {new_milkers}!")
        return redirect(url_for('owner.add_own'))

    return render_template('owner/add_own.html', form=form, flash=form.errors)


@owner.route('/remove_own')
@login_required
def remove_own():
    return render_template('info.html')


@owner.route('/list_own', methods=['GET', 'POST'])
@login_required
def list_own():
    form = DeleteCustForm()
    print(form.data, "sdsd")
    print(form.validate_on_submit(), "v")
    error = []
    owner_list = CowOwner.query.order_by(CowOwner.owner_id).all()
    if form.validate_on_submit():
        owner_id_del = form.checkbox.raw_data
        if owner_id_del:
            print(f"Owner Id's to update {owner_id_del}")
            if len(owner_id_del) > 5:
                flash("Please do not update more than 5 Customers at a time", category='error')
                return redirect(url_for('owner.list_own'))
            else:
                try:
                    id = [int(ids.split(':')[0]) for ids in owner_id_del]
                    owner_id = [int(ids.split(':')[1]) for ids in owner_id_del]
                    # print(id)
                    # print(owner_id)
                    total_del = CowOwner.query.filter(CowOwner.owner_id.in_(owner_id), CowOwner.id.in_(id))
                    print("outside", total_del.all())
                except:
                    flash("Not able to update some customers. Try one by one!", category='error')
                else:
                    if len(total_del.all()) == len(owner_id_del):
                        owners_active = ",".join([owner.name for owner in total_del if owner.active])
                        owners_inactive = ",".join([owner.name for owner in total_del if not owner.active])
                        for o in total_del:
                            print("Inside", total_del.all())
                            if o.active is True:
                                print(total_del.filter(CowOwner.id == o.id).all())
                                total_del.filter(CowOwner.id == o.id). \
                                    update({"active": False})
                                print("tue", o.active, o.name)
                                try:
                                    print("Trying to commit")
                                    db.session.commit()
                                except:
                                    print(f"Failed to Delete {o.name}. RollingBack!")
                                    db.session.rollback()
                                    flash("Error in Deleting Owner!.Reach Admin", category='error')
                            else:
                                print("false", total_del.filter(CowOwner.id == o.id).all())
                                total_del.filter(CowOwner.id == o.id). \
                                    update({"active": True})
                                print("False", o.active, o.name)
                                try:
                                    print("Trying to commit")
                                    db.session.commit()
                                except:
                                    print(f"Failed to Delete {o.name}. RollingBack!")
                                    db.session.rollback()
                                    flash("Error in Deleting Owner!.Reach Admin", category='error')

                        print(owners_active, "gh", owners_inactive)
                        active = f"Owners {owners_active} Deactivated Successfully!"
                        inactive = f"Owners {owners_inactive} Activated Successfully!"
                        if owners_active and not owners_inactive:
                            flash(active)
                        elif owners_inactive and not owners_active:
                            flash(inactive)
                        else:
                            flash(active), flash(inactive)

                        return redirect(url_for('owner.list_own'))

    for error, message in form.errors.items():
        flash(f"{error.capitalize()} : {message[0]}", category='error')

    header = ['✓', 'CustomerId', 'Name', 'Place', 'Number of Cows', 'Milker', 'Active']
    tm_header = ['✓', 'வா.என்', 'பெயர்', 'ஊர்', 'கறவை மாடுகள்', 'க.என்', 'செயல்பாடு']
    return render_template('owner/list_own.html',
                           header=header,
                           tm_header=tm_header,
                           owner_list=owner_list,
                           flash=form.errors,
                           form=form)


@owner.route('/liab_own/<int:own_id>', methods=['GET', 'POST'])
@login_required
def liab_own(own_id):
    form = EditUserForm()
    day = today_date
    # milker_names=None
    print(own_id)
    # form.milker_id.choices = milker_choice()

    owner_query = CowOwner.query.filter(CowOwner.owner_id == own_id)
    owner = owner_query.first_or_404()
    print(owner.name)

    loan_ids = Loan.query.filter(Loan.owner_id == owner.owner_id).all()

    print("Form validation", form.validate_on_submit())
    print(form.kcc_loan.data, "kcc")
    print(form.dairy_loan.data, "dairy")
    print (loan_ids,"Loan Details")
    loan_data = [loan_id.loan_details() for loan_id in loan_ids]
    print (loan_data,"loan data")

    milker_names = owner.milker_list()
    # milker_of_owner = [own.milker_id for own in owner_query.all()]
    # milker_names = Milkers.query.\
    #     filter(Milkers.milker_id.in_(milker_of_owner)).all()

    month = today_date.replace(day=1)
    ledger_obj = WholeMonthData(month)
    loan_details_for_month = ledger_obj.milk_data_query.filter(Milk.owner_id == own_id).first()
    print(form.validate_on_submit(), "form valid status")

    if form.validate_on_submit():
        print(form.email.data, "email")
        print(form.phone_number.data, "phone")
        email_check = check_own_email(form.email.data, owner.owner_id)
        phone_check = check_own_phone(form.phone_number.data, owner.owner_id)
        if not email_check and not phone_check:
            CowOwner.query.filter(CowOwner.owner_id == own_id).update({
                'name': form.name.data,
                'surname': form.surname.data,
                'place': form.place.data,
                'cows': form.cows.data,
                'phone_number': form.phone_number.data,
                'address_line2': form.address_line2.data,
                'pincode': form.pincode.data,
                'dairy_loan': form.dairy_loan.data,
                'kcc_loan': form.kcc_loan.data,
                'email': form.email.data,
                'country': form.country.data,
                'state': form.state.data,

            })

            if form.picture.data:
                owner_name = owner.owner_id
                pic = add_profile_pic(form.picture.data, owner_name)
                CowOwner.query.filter(CowOwner.owner_id == own_id).update({
                    'profile_pic_name': pic
                }
                )
                # own.profile_pic_name = pic
            if form.loan_amount.data:
                if form.loan_start_date.data and form.loan_end_date.data:
                    loan_data = Loan(
                        form.loan_amount.data,
                        form.loan_type.data,
                        own_id,
                        form.loan_start_date.data,
                        form.loan_end_date.data
                    )
                    db.session.add(loan_data)
                else:
                    flash(f"Loan Start and End Date are Mandatory")
                try:
                    db.session.commit()
                except:
                    flash(f"Error in updating Loan")
                else:
                    flash(f"Loan data added Successfully")
            try:
                db.session.commit()
            except:
                db.session.commit() # to debug
                flash(f"Unknown Error in updating profile")
            else:
                flash(f"Profile Updated Successfully")
        elif email_check:
            flash(f"Email {form.email.data} is already taken!")
        elif phone_check:
            flash(f"Mobile number {form.phone_number.data} is already taken!")

        return redirect(url_for('owner.liab_own', own_id=own_id))

    elif request.method == 'GET':

        form.name.data = owner.name
        form.place.data = owner.place
        form.email.data = owner.email
        form.cows.data = owner.cows
        form.surname.data = owner.surname
        form.pincode.data = owner.pincode
        form.phone_number.data = owner.phone_number
        form.address_line2.data = owner.address_line2
        form.kcc_loan.data = owner.kcc_loan if owner.kcc_loan else 0
        form.dairy_loan.data = owner.dairy_loan if owner.dairy_loan else 0
        form.country.data = owner.country
        form.state.data = owner.state
        milker_names = owner.milker_list()
        print(owner.kcc_loan,"Kcc Loan Data")
        print(owner.dairy_loan, "Dairy Loan Data")
    # print (owner.cows,"cows")
    # print (form.name.data)

    for error, message in form.errors.items():
        print(error, message, form.pincode.data)
        flash(f"{error.capitalize()} : {message[0]}", category='error')

    profile_image = url_for('static',
                            filename='profile_pics/' + owner.profile_pic_name) if owner.profile_pic_name else None

    return render_template('owner/liab_own.html',
                           form=form,
                           day=day,
                           profile_image=profile_image,
                           flash=form.errors,
                           milker_names=milker_names,
                           loan_details_for_month=loan_details_for_month,
                           owner=owner,
                           loan_data=loan_data
                           )

try:
    from Paalkanakku import app, db
    from Paalkanakku.models import Milkers, CowOwner
    from Paalkanakku.milkers.forms import AddMilkForm, DeleteMilkForm, milker_data

except:
    from Paalkanakku.Paalkanakku import app, db
    from Paalkanakku.Paalkanakku.models import Milkers, CowOwner
    from Paalkanakku.Paalkanakku.milkers.forms import AddMilkForm, DeleteMilkForm

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

milker = Blueprint('milker', __name__)



@milker.route('/add_ml', methods=['GET', 'POST'])
@login_required
def add_milker():

    form = AddMilkForm()

    print(form.data)
    print (form.validate_on_submit())
    print (form.form_errors)
    if form.validate_on_submit():
        name = form.name.data
        place = form.place.data
        bike = form.bike.data
        salary = form.salary.data
        milker_data = Milkers(
            name=name,
            place=place,
            bike=bike,
            salary=salary,
            #owner_id=owner_id,
        )
        db.session.add(milker_data)
        print(milker_data)
        try:
            print("Trying to commit")
            db.session.commit()
        except:
            print("Failed to commit")
            db.session.rollback()
            flash("Error in Adding New Milker!")
        else:
            flash(f"Milker {milker_data.name} is Successfully Added!")
            return redirect(url_for('milker.add_milker'))

    return render_template('milker/add_milker.html', form=form, flash=form.errors)

"""
@milker.route('/link_ml', methods=['GET', 'POST'])
@login_required
def link_milker():

    form = AddMilkForm()
    owners = CowOwner.query.all()
    choices = [(o.owner_id, str(o.owner_id)+ ' '+o.name+' '+o.place) for o in owners]
    form.owner_id.choices = choices

    print(form.data)
    print (form.validate_on_submit())
    print (form.form_errors)
    if form.validate_on_submit():
        name = form.name.data
        place = form.place.data
        bike = form.bike.data
        salary = form.salary.data
        owner_id = form.owner_id.data

        milker_data = Milkers.query.filter_by(name=name, place=place).first()
        print (milker_data,"dad")
        if milker_data is not None:
            print ("Milker already there")
            name = form.name.data
            place = form.place.data
            bike = form.bike.data
            salary = form.salary.data
            #owner_id = form.owner_id.data
            milker_data.owner_id = owner_id
            db.session.add(milker_data)
            try:
                print("Trying to commit")
                db.session.commit()
            except:
                print("Failed to commit")
                db.session.rollback()
                flash("Error in Adding New Milker!")
            else:
                flash(f"Milker {milker_data.name} is Successfully linked to {owner_id}!")
                return redirect(url_for('milker.add_milker'))

        else:
            milker_data = Milkers(
                name=name,
                place=place,
                bike=bike,
                salary=salary,
                owner_id=owner_id,
            )
            db.session.add(milker_data)
            print(milker_data)
            try:
                print("Trying to commit")
                db.session.commit()
            except:
                print("Failed to commit")
                db.session.rollback()
                flash("Error in Adding New Milker!")
            else:
                flash(f"Milker {milker_data.name} Added Successfully!")
                return redirect(url_for('milker.add_milker'))

    return render_template('milker/add_milker.html', form=form, flash=form.errors)
"""

@milker.route('/remove_ml')
def remove_milker():
    return render_template('remove_milker.html')


@milker.route('/list_ml',methods=['GET', 'POST'])
def list_milker():

    form = DeleteMilkForm()
    error = []
    if form.validate_on_submit():
        milker_id_del = form.checkbox.raw_data
        if milker_id_del:
            print (f"Milker Id's to update {milker_id_del}")
            if len(milker_id_del)>5:
                error.append("Please do not update more than 5 Milkers at a time")
                return redirect(url_for('milker.list_milker'))
            else:
                try:
                    total_sel_milker = Milkers.query.filter(Milkers.milker_id.in_(milker_id_del))
                except:
                    error("Not able to deactivate some Mikers. Try one by one!")
                else:
                    if len(total_sel_milker.all()) == len(milker_id_del):
                        milker_active = ",".join([milker.name for milker in total_sel_milker if milker.active])
                        milker_inactive = ",".join([milker.name for milker in total_sel_milker if not milker.active])
                        for m in total_sel_milker:
                            print (total_sel_milker.all())
                            if m.active is True:
                                total_sel_milker.filter(Milkers.milker_id==m.milker_id).\
                                    update({"active": False})
                                print ("tue",m.active,m.name)
                                db.session.commit()
                            else:
                                total_sel_milker.filter(Milkers.milker_id==m.milker_id).\
                                    update({"active": True})
                                print ("False",m.active,m.name)
                                db.session.commit()
                                print("Committed")

                        print (milker_active,"gh",milker_inactive)
                        active = f"Mikers {milker_active} Deactivated Successfully!"
                        inactive = f"Mikers {milker_inactive} Activated Successfully!"
                        if milker_active and not milker_inactive:
                            flash(active)
                        elif milker_inactive and not milker_active:
                            flash(inactive)
                        else:
                            flash(active),flash(inactive)

                        return redirect(url_for('milker.list_milker'))

    for error,message in form.errors.items():
        flash(f"{error.capitalize()} : {message[0]}", category='error')

    milker_list = milker_data()[0]
    print (milker_list)
    #header = ['', 'MilkerId', 'Name', 'Place', 'Salary', 'Bike', 'OwnerId']
    header = ['', 'MilkerId', 'Name', 'Place', 'Salary', 'Bike','Active']
    return render_template('milker/list_milker.html',
                           header=header,
                           milker_list=milker_list,
                           flash=form.errors,
                           form=form)


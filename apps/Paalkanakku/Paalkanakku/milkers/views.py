try:
    from Paalkanakku import app, db
    from Paalkanakku.models import Milkers, CowOwner
    from Paalkanakku.milkers.forms import AddMilkForm, DeleteMilkForm

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
            print (f"Milker Id's to delete {milker_id_del}")
            if len(milker_id_del)>5:
                error.append("Please do not delete more than 5 Milkers at a time")
                return redirect(url_for('milker.list_milker'))
            else:
                try:
                    total_del = Milkers.query.filter(Milkers.milker_id.in_(milker_id_del)).all()
                except:
                    error("Not able to delete some Mikers. Try one by one!")
                else:
                    if len(total_del) == len(milker_id_del):
                        milkers = ",".join([owner.name for owner in total_del])
                        Milkers.query.filter(Milkers.milker_id.in_(milker_id_del)).delete()
                        try:
                            print("Trying to commit")
                            db.session.commit()
                        except:
                            print("Failed to Delete. RollingBack!")
                            db.session.rollback()
                            flash("Error in Deleting Milker!.Reach Admin")
                        else:
                            flash(f"Mikers {milkers} Deleted Successfully!")
                            return redirect(url_for('milker.list_milker'))
                    return redirect(url_for('milker.list_milker'))

    milker_list = Milkers.query.all()
    print (milker_list)
    #header = ['', 'MilkerId', 'Name', 'Place', 'Salary', 'Bike', 'OwnerId']
    header = ['', 'MilkerId', 'Name', 'Place', 'Salary', 'Bike']
    return render_template('milker/list_milker.html',
                           header=header,
                           milker_list=milker_list,
                           flash=form.errors,
                           form=form)


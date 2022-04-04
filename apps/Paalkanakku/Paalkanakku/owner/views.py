
try:
    from Paalkanakku import app, db
    from Paalkanakku.models import Milkers, CowOwner
    from Paalkanakku.owner.forms import AddCustForm, DeleteCustForm

except:
    from Paalkanakku.Paalkanakku import app, db
    from Paalkanakku.Paalkanakku.models import Milkers, CowOwner
    from Paalkanakku.Paalkanakku.owner.forms import AddCustForm, DeleteCustForm

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

owner = Blueprint('owner', __name__)


def check_milker(name,place):
    """
    To return the details of the owners available already
    """
    owner_detail = CowOwner.query.filter_by(name=name,place=place).all()
    if owner_detail:
        return owner_detail


@owner.route('/add_own', methods=['GET', 'POST'])
@login_required
def add_own():
    form = AddCustForm()

    milkers = Milkers.query.all()
    choices = [(str(o.milker_id), o.name) for o in milkers]
    print(choices)
    form.milker_id.choices = choices

    print(form.data)
    if form.validate_on_submit():
        total_rows = CowOwner.query.count()
        name = form.name.data
        place = form.place.data
        owner_id = total_rows+1000
        x=0
        objects = []
        new_milkers = []
        for milker in form.milker_id.data:
            x+=1
            print (x,"x")
            owners_list = check_milker(name, place)
            milker = int(milker)
            print (owners_list, "printing out")
            print(milker, "milker check")

            if owners_list is None:
                new_milkers.append(milker)
                print(owners_list, "Inside")
                owner_data = CowOwner(
                    owner_id= owner_id,
                    name= name,
                    place=place,
                    num_cows=form.cows.data,
                    milker_id=milker
                )
                objects.append(owner_data)
                print(owner_data,"Hello there")
            else:
                milker_list = [owner.milker_id for owner in owners_list]
                owner_id = owners_list[0].owner_id
                print (owner_id)
                print (milker_list)
                if milker not in milker_list:
                    new_milkers.append(milker)
                    owner_data = CowOwner(
                        owner_id=owner_id,
                        name=name,
                        place=place,
                        num_cows=form.cows.data,
                        milker_id=int(milker)
                    )
                    #db.session.add(owner_data)
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

            print ("Ended for")

        try:
            print (objects,"total obj")
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


@owner.route('/list_own',methods=['GET','POST'])
@login_required
def list_own():

    form = DeleteCustForm()
    print (form.data,"sdsd")
    print(form.validate_on_submit(), "v")
    error = []
    if form.validate_on_submit():
        owner_id_del = form.checkbox.raw_data
        if owner_id_del:
            print (f"Owner Id's to delete {owner_id_del}")
            if len(owner_id_del)>5:
                flash("Please do not delete more than 5 Customers at a time",category='error')
                return redirect(url_for('owner.list_own'))
            else:
                try:
                    id = [int(ids.split(':')[0]) for ids in owner_id_del]
                    owner_id = [int(ids.split(':')[1]) for ids in owner_id_del]
                    #print(id)
                    #print(owner_id)
                    total_del = CowOwner.query.filter(CowOwner.owner_id.in_(owner_id), CowOwner.id.in_(id)).all()
                    print(total_del)
                except:
                    flash("Not able to delete some customers. Try one by one!",category='error')
                else:
                    if len(total_del) == len(owner_id_del) :
                        owners = ",".join([owner.name for owner in total_del])
                        #CowOwner.query.filter(CowOwner.owner_id.in_(owner_id_del)).delete()
                        CowOwner.query.filter(CowOwner.owner_id.in_(owner_id), CowOwner.id.in_(id)).delete()
                        try:
                            print("Trying to commit")
                            db.session.commit()
                        except:
                            print("Failed to Delete. RollingBack!")
                            db.session.rollback()
                            flash("Error in Deleting Owner!.Reach Admin",category='error')
                        else:
                            flash(f"Owners {owners} is Successfully deleted!")
                            return redirect(url_for('owner.list_own'))
                    return redirect(url_for('owner.list_own'))


    owner_list = CowOwner.query.all()
    header = ['', 'CustomerId', 'Name', 'Place', 'Number of Cows','Milker']
    return render_template('owner/list_own.html',
                           header=header,
                           owner_list=owner_list,
                           flash=form.errors,
                           form=form)

from puppyadoption import Blueprint,render_template,redirect,url_for,flash
from puppyadoption import db,login_required
from puppyadoption.puppies.models import Puppy
from puppyadoption.puppies.forms import Add_form,Del_form

puppies_blueprint = Blueprint('puppies',__name__,template_folder='templates/puppies')


@puppies_blueprint.route('/addpup', methods=['GET','POST'])
@login_required
def addpup():
    form = Add_form()

    if form.validate_on_submit():

        name = form.name.data

        new_pup = Puppy(name)

        db.session.add(new_pup)
        db.session.commit()
        return redirect(url_for('puppies.listpup'))

    return render_template("addpup.html",form=form)


@puppies_blueprint.route('/listpup')
@login_required
def listpup():
    puppies = Puppy.query.all()

    return render_template("listpup.html",puppies=puppies)


@puppies_blueprint.route('/delpup',methods=['GET', 'POST'])
@login_required
def delpup():

    form = Del_form()

    if form.validate_on_submit():
        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for('puppies.listpup'))
    return render_template("delpup.html",form=form)



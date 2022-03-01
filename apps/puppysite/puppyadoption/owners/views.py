from puppyadoption import Blueprint,render_template,redirect,url_for,flash,login_required
from puppyadoption import db
from puppyadoption.owners.models import Owner
from puppyadoption.owners.forms import Add_form

owners_blueprint = Blueprint('owners',__name__,template_folder='templates/owners')


@owners_blueprint.route('/add', methods=['GET','POST'])
@login_required
def ownpup():
    form = Add_form()

    if form.validate_on_submit():
        name = form.name.data
        id = form.id.data

        new_own = Owner(name,id)

        db.session.add(new_own)
        db.session.commit()
        flash(f"Puppy {id} is adopted by {name}")
        return redirect(url_for("puppies.listpup"))
    return render_template("ownpup.html",form=form)

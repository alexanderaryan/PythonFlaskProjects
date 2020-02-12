from dress_me.dressme.attireshuffler.forms import FemaleForm,MainMaleForm,ShuffleForm
from dress_me.dressme import app, render_template, redirect, Blueprint,url_for,request, session
from dress_me.dressme.attireshuffler import cal_dress


dress_print = Blueprint('dress_print',__name__)


@dress_print.route('/male',methods=['GET','POST'])
def male():
    form=MainMaleForm()

    if form.validate_on_submit():
        shirt=[n['shirt'] for n in form.attires.data]
        pants=[n['pants'] for n in form.attires.data]
        dress=cal_dress.create_combo(shirt,pants)
        session['dress_list']=dress
        return redirect(url_for('dress_print.shuffled'))

    return render_template("male.html",form=form)


@dress_print.route('/female')
def female():
    form = FemaleForm()
    return render_template('female.html', form=form)


@dress_print.route('/shuffled', methods=['GET', 'POST'])
def shuffled():
    form = ShuffleForm()
    return render_template("shuffled.html", form=form)


@dress_print.route('/main_list', methods=['GET', 'POST'])
def main_list():
    if request.method == 'POST':
        print(request.form.getlist('attire'))
        print(cal_dress.main_combo)
        return "<h1>request.args</h1>"




from dress_me.dressme.attireshuffler.forms import FemaleForm,MainMaleForm,ShuffleForm,MainFemaleForm
from dress_me.dressme import app, render_template, redirect, Blueprint,url_for,request, session
from dress_me.dressme.attireshuffler import cal_dress


dress_print = Blueprint('dress_print',__name__)

dress = []

@dress_print.route('/male',methods=['GET','POST'])
def male():
    form = MainMaleForm()
    global dress
    dress = []
    if form.validate_on_submit():
        shirt=[n['shirt'] for n in form.attires.data]
        print (shirt,'shirt')
        pants=[n['pants'] for n in form.attires.data if n['pants'] != '']
        print(pants,'pants')
        #global dress
        dress=cal_dress.create_combo(shirt,pants)
        
        return redirect(url_for('dress_print.shuffled'))

    return render_template("male.html",form=form)


@dress_print.route('/female',methods=['POST','GET'])
def female():
    form = MainFemaleForm()
    date_form = ShuffleForm()
    global dress
    dress = []
    if form.validate_on_submit():
        dress = [n['attire'] for n in form.attires.data]
        print (dress)
        print (date_form.from_date.data)
        print(date_form.to_date.data)
        return redirect(url_for('dress_print.shuffled'))

    return render_template('female.html', form=form, date_form=date_form)


@dress_print.route('/shuffled/', methods=['GET', 'POST'])
def shuffled():
    form = ShuffleForm()
    if form.validate_on_submit():
    #if request.method == 'POST':
        print (form.from_date.data)
        print(form.to_date.data)
        remove_dress = [tuple(dre.split(' with ')) for dre in request.form.getlist('attire')]
        print (remove_dress,'x')
        removed = cal_dress.remove_the_dress(dress, remove_dress)
        print (removed,'removed list')
        session['dress_list'] = removed
        to_roaster = cal_dress.alter_the_sequence(removed)
        print (to_roaster)
        print (cal_dress.main_combo,'main')
        cal_dress.create_calendar((int(form.from_date.data[6:]), int(form.from_date.data[3:5]),\
                                   int(form.from_date.data[:2])), \
                                  (int(form.to_date.data[6:]), int(form.to_date.data[3:5]),\
                                   int(form.to_date.data[:2])), (5, 6))
        final_result = cal_dress.create_schedule()
        print (final_result,'final_result')
        return render_template("main_list.html",final_result = final_result,x='12' )
    return render_template("shuffled.html", form=form,dress=dress)


"""@dress_print.route('/main_list', methods=['GET', 'POST'])
def main_list():
    if request.method == 'GET':
        remove_dress=[tuple(dress.split(' with ')) for dress in request.form.getlist('attire')]
        print (remove_dress,'x')
        removed=cal_dress.remove_the_dress(dress,remove_dress)
        print (removed,'removed list')
        session['dress_list'] = removed
        to_roaster = cal_dress.alter_the_sequence(removed)
        print (to_roaster)
        print (cal_dress.main_combo,'main')
        cal_dress.create_calendar((2020, 2, 7), (2020, 8, 29), (5, 6))
        final_result = cal_dress.create_schedule()
        print (final_result,'final_result')
        return render_template("main_list.html",final_result = final_result,x='12' )



"""
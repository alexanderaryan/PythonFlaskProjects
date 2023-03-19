from sqlalchemy import func
import yaml
try:
    from Paalkanakku import app, db
    from Paalkanakku.models import User
    from Paalkanakku.users.forms import RegistrationForm, UpdateUserForm, LoginForm
    from Paalkanakku.users.picture_handler import add_profile_pic
    #from Paalkanakku.config import google
    from Paalkanakku.config import sheet_config
    from Paalkanakku.milkdata import config_data
except:
    from Paalkanakku.Paalkanakku import app, db
    from Paalkanakku.Paalkanakku.models import User
    from Paalkanakku.Paalkanakku.users.forms import RegistrationForm, UpdateUserForm, LoginForm
    from Paalkanakku.Paalkanakku.users.picture_handler import add_profile_pic
    #from Paalkanakku.Paalkanakku.config import google
    from Paalkanakku.Paalkanakku.config import sheet_config
    from Paalkanakku.Paalkanakku.milkdata import config_data

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

users = Blueprint('users', __name__)


@users.route('/reg', methods=['POST','GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                username=form.username.data,
                password=form.password.data
                )
        db.session.add(user)
        try:
            print ("re")
            db.session.commit()
        except:
            print("red")
            db.session.rollback()
            flash("Your email/username is already registered.Try Log in",category="error")
            return render_template('register.html', form=form, flash=form.errors)
        else:
            flash("You are Successfully Registered!")
            return redirect(url_for('users.login'))

    return render_template('register.html', form=form, flash=form.errors)


@users.route('/login', methods=['POST','GET'])
def login():

    form = LoginForm()
    error = []

    if form.validate_on_submit():

        user = User.query.filter(func.lower(User.email) == func.lower(form.email.data)).first()
        username = User.query.filter(func.lower(User.username) ==func.lower(form.email.data)).first()
        print ("hello1", user, username)
        try:
            if user:
                if user.check_password(form.password.data):
                    login_user(user)
            elif username:
                if username.check_password(form.password.data) and username is not None:
                    login_user(username)
            else:
                print("I came here3")
                flash("Email or password is wrong")
                return render_template('login.html', form=form)
        except:
            error.append('Oho!')
            flash("Email is not Registered.")
            return render_template('login.html', form=form)
        else:
            flash("You are logged in!")
            print ("Logged in ", request.args.get('next'))
            next_page = request.args.get('next')
            if next_page is None or not next_page[0] == '/':
                next_page = url_for('core.index')
            return redirect(next_page)

    return render_template('login.html',form=form,flash=form.errors,error=error)


@users.route('/logout')
def logout():
    logout_user()
    flash("You are logged out!")
    return redirect(url_for('core.index'))


@users.route('/account', methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    print (form.data,"after")

    if form.validate_on_submit():
        print(form.milker_toggle.data,"form data")

        data = config_data()
        if form.milker_toggle.data == 'no':
            data['no_milker'] = True
        else:
            data['no_milker'] = False

        with open(sheet_config, 'w') as yaml_file:
            yaml_file.write(yaml.dump(data, default_flow_style=False))

        if form.picture.data:

            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            #print ("Inside valida form", pic)
            current_user.profile_image = pic

        try:
            current_user.username = form.username.data
            db.session.commit()
        except:
            flash(f"Username taken already")
        else:
            try:
                current_user.email = form.email.data
                db.session.commit()
            except:
                flash(f"Email registered already")
            else:
                db.session.commit()
                flash("Your Profile Updated!")

        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        #print ("form invalid")
        form.username.data = current_user.username
        form.email.data = current_user.email

    no_milker = config_data()['no_milker']
    print(no_milker, "nomilker")
    if no_milker is True:
        form.milker_toggle.data="no"
    else:
        form.milker_toggle.data = "yes"

    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    #print (profile_image,"profile_pic name")
    return render_template('account.html',
                           profile_image=profile_image,
                           no_milker=no_milker,
                           form=form,
                           flash=form.errors)






"""
@users.route('/log')
def index():
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    #print(resp.json())
    email = resp.json()['email']
    return render_template('index.html', email=email)


@users.route('/login/google')
def login():
    if not google.authorized:
        return render_template(url_for('google.login'))
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    #print(resp.json())
    email = resp.json()['email']
    return render_template('index.html', email=email)
"""